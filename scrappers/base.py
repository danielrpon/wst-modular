import logging
import sys
import time
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import (
    ElementNotInteractableException,
    JavascriptException,
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from structures.products import Product

logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


class BaseScrapper:
    # Config
    url = None
    pais = None
    fuente = None
    search_placeholder = "guaro"
    page_placeholder = "pagenum"
    stop_behavior = None
    page_type = None
    product_class = Product
    pages = None
    products = None
    products_per_page = 1
    page_number = 0
    max_time_out = 60
    do_scroll = False
    browser = None
    show_browser = True
    verbose = False

    # Selectors
    product_selector = None
    product_count_selector = None
    pagination_selector = None
    sku_selector = None
    ean_selector = None
    brand_selector = None
    product_name_selector = None
    regular_price_selector = None
    discount_price_selector = None
    image_selector = None

    # Private Access
    search_phrase = None

    # Opciones de páginado
    STOP_IF_NO_PRODUCTS = 1
    STOP_IF_SELECTOR_NOT_PRESENT = 2
    STOP_IF_PRODUCT_COUNT_REACHED = 3
    STOP_IF_PAGE_COUNT_REACHED = 4
    STOP_IF_SELECTOR_IS_DISABLED = 5

    # Opciones de navegación
    SINGLE_PAGE = 1
    SSR_PAGE = 2

    # Opciones del Driver
    USE_CHROME = 1
    USE_FIREFOX = 2

    # Opciones de Visualización
    SHOW_BROWSER = False

    _headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    }
    selenium_driver = None

    def __init__(self, *args, **kwargs):
        for attribute, value in kwargs.items():
            setattr(self, attribute, value)

        if self.verbose:
            logging.getLogger().setLevel(logging.INFO)

    def get_products(self, search_phrase):

        # TODO Cachear las Variable

        logging.info(f"Obteniendo Productos de {self.fuente}")
        # Guardar la frase de busqueda
        self.search_phrase = search_phrase
        self.products = []

        # Obtener las Paginas
        for page in self.get_pages_source():

            soup = BeautifulSoup(page, "html.parser")
            # Procesamiento de Campos

            # por cada producto en la pagina extraer los campos
            for product in soup.select(self.product_selector):
                product_data = self.get_product_data(product)
                self.products.append(product_data)
        # Close Browser
        self.get_selenium_driver().quit()
        return self.products

    def get_pages_source(self):

        logging.info("Obteniendo Paginas")
        driver = self.get_selenium_driver()
        self.pages = []

        # Obtener las paginas

        has_products = True

        while has_products:
            logging.info(f"Obteniendo Pagina {self.page_number+1}")
            page_source = None

            if not len(self.pages):
                driver.get(self.get_search_url())

            # Controlar el tipo de página
            if self.page_type == self.SSR_PAGE:
                if len(self.pages):
                    driver.get(self.get_search_url())
                self.load_page(driver)
            elif self.page_type == self.SINGLE_PAGE:
                self.load_page(driver)
                self.get_current_page_number()
                # Ir a hacer click en el boton de ver más/cargar más
                try:
                    driver.execute_script(
                        f'document.querySelector("{self.pagination_selector}").click();'
                    )
                except JavascriptException:
                    logging.warning(f"{self.fuente}-> No se encontró un selector de página siguiente.")


            page_source = driver.page_source

            # Detener
            if self.stop_behavior == self.STOP_IF_NO_PRODUCTS:
                # verificar si hay productos
                soup = BeautifulSoup(page_source, "html.parser")
                total_products = len(soup.select(self.product_selector))
                has_products = bool(total_products)
            elif self.stop_behavior == self.STOP_IF_SELECTOR_NOT_PRESENT:
                soup = BeautifulSoup(page_source, "html.parser")
                has_products = bool(len(soup.select(self.pagination_selector)))
            # TODO detenerse si alcanza la cantidad total de productos
            elif self.stop_behavior == self.STOP_IF_PRODUCT_COUNT_REACHED:
                pass
            elif self.stop_behavior == self.STOP_IF_PAGE_COUNT_REACHED:
                if self.get_current_page_number() >= self.get_page_count():
                    has_products = False
            elif self.stop_behavior == self.STOP_IF_SELECTOR_IS_DISABLED:
                soup = BeautifulSoup(page_source, "html.parser")
                has_products = (
                    not "disabled"
                    in soup.select(self.pagination_selector)[0].attrs.keys()
                )

            # Agregar Html de la pagina
            if self.page_type == self.SINGLE_PAGE:
                if not len(self.pages):
                    self.pages.append(page_source)
                self.pages[0] = page_source
            elif self.page_type == self.SSR_PAGE:
                if has_products:
                    self.pages.append(page_source)

        # 2.1 Caso 2 click en selector css (Cargar más: Exito, Farmatodo)
        return self.pages

    def load_page(self, driver):
        """Espera a la carga del sitio y realiza Scroll para cargar productos."""
        # Scroll
        if self.do_scroll:
            scroll_height = driver.execute_script("return document.body.scrollHeight")
            y_pos = 0
            while y_pos < scroll_height:
                y_pos += 100
                driver.execute_script(f"window.scroll(0,{y_pos})")
                scroll_height = driver.execute_script(
                    "return document.body.scrollHeight"
                )
                time.sleep(0.2)

        try:
            WebDriverWait(driver, self.max_time_out, poll_frequency=0.5).until(
                expected_conditions.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, self.product_selector)
                )
            )
        except TimeoutException:
            logging.warning(f"{self.fuente}-> No se encontraron productos en la página {self.page_number}")

    def get_current_page_number(self):
        """Retorna la siguiente página para usar en URLS."""
        self.page_number += 1
        return self.page_number

    def get_page_count(self,total_products):
        """Retornar la cantidad de páginas totales que puede contener la consulta."""
        pass

    def get_search_url(self):
        """Reemplaza el valor de la palabra de busqueda."""
        return self.url.replace(self.search_placeholder, self.search_phrase).replace(
            self.page_placeholder, str(self.get_current_page_number())
        )

    def get_selenium_driver(self):
        if self.selenium_driver is None:
            service = None

            # TODO verificar si el usuario quiere modo oculto

            if self.browser in [None, self.USE_CHROME]:
                options = ChromeOptions()
                options.page_load_strategy = "normal"
                options.add_argument(
                    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0")
                options.add_experimental_option("excludeSwitches", ["enable-logging"])
                options.add_argument("--disable-gpu")
                if not self.show_browser:
                    options.add_argument("--headless")
                    options.add_argument("--no-sandbox")

                service = ChromeService(executable_path=ChromeDriverManager().install())
                self.selenium_driver = webdriver.Chrome(
                    service=service,
                    options=options,
                    desired_capabilities=DesiredCapabilities.CHROME.copy(),
                )

            if self.browser == self.USE_FIREFOX:
                options = FirefoxOptions()
                options.page_load_strategy = "normal"
                options.add_argument(
                    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0")

                if not self.show_browser:
                    options.add_argument("--headless")
                    options.add_argument("--no-sandbox")

                service = FirefoxService(executable_path=GeckoDriverManager().install())
                self.selenium_driver = webdriver.Firefox(
                    service=service,
                    options=options,
                    desired_capabilities=DesiredCapabilities.FIREFOX.copy(),
                )
        return self.selenium_driver

    def get_product_data(self, product):
        """Recorre los selectores en busca de sus valores."""
        # Obtener una lista de atributos de selectores
        # TODO mover a una constante de clase
        attributes = [
            "sku_selector",
            "ean_selector",
            "brand_selector",
            "product_name_selector",
            "regular_price_selector",
            "discount_price_selector",
            "image_selector",
        ]

        selector_data = {}
        # Obtener el valor de cada selector
        for attribute in attributes:
            if getattr(self, attribute, None) is not None:
                selector_data[attribute] = product.select_one(
                    getattr(self, attribute, None)
                )
            else:
                selector_data[attribute] = None

        return self.product_class(**selector_data)


class D1Scrapper(BaseScrapper):
    def get_page_count(self):
        """Personalización para dejar solo 1 Pagina"""
        return 1

class OlimpicaScrapper(BaseScrapper):
    def get_page_count(self,total_products):
        """Personalización para paginado"""
        return int(total_products/self.products_per_page)


class MercadolibreScrapper(BaseScrapper):
    def get_page_count(self,total_products):
        """Personalización para paginado"""
        return int(total_products/self.products_per_page)

    def get_search_url(self):
        """Reemplaza el valor de la palabra de busqueda."""
        return self.url.replace(self.search_placeholder, self.search_phrase).replace(
            self.page_placeholder, str(self.get_current_page_number())
        )

    def get_current_page_number(self):
        """Retorna la siguiente página para usar en URLS."""
        self.page_number += 1
        return self.page_number