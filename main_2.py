# Evaluar ingresar WST https://gloss.com.ec/
# Evaluar scraping HomeCenter, HomeCentry o falabela. Priorizar
# INCLUIR ESIKA, ORIFLAME
# https://pe.oriflame.com/search?query=desodorante
# https://esika.tiendabelcorp.com/co/search/?text=crema

# Importaciones
from ast import Continue
from asyncio.windows_events import NULL
from distutils.filelist import findall
import time
import math
import unicodedata
from bs4 import BeautifulSoup
import csv, os, datetime
import re
import json
from selenium import webdriver
from urllib.parse import urlparse, parse_qs
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    JavascriptException,
    ElementNotInteractableException,
    NoSuchElementException,
)

# Navegador Web
options = Options()
options.page_load_strategy = "normal"

# sÍ lo quiero ver visible en chrome
# options.add_argument("--headless")
# options.add_argument("--no-sandbox")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(
    "C:\\Users\\restreda\\Desktop\\DRN\\WST\\chromedriver",
    options=options,
    service_log_path="C:\\Users\\restreda\\Desktop\\DRN\\WST\\log.txt",
)
options.add_argument("--disable-in-process-stack-traces")
options.add_argument("--disable-logging")


# Configuracion
root_dir = "C:\\Users\\restreda\\Desktop\\DRN\\WST\\"
dest_folder = "C:\\Users\\restreda\\Desktop\\DRN\\WST\\"
input_file_path = os.path.join(root_dir, "input.csv")
fuentes = {
    "exito": {"pais": "Colombia"},
    "D1": {"pais": "Colombia"},
    "ARA": {"pais": "Colombia"},
    "jumbo": {"pais": "Colombia"},
    "avoncol": {"pais": "Colombia"},
    "mercalicol": {"pais": "Colombia"},
    "farmatodo": {"pais": "Colombia"},
    "wong": {"pais": "Peru"},
    "inkafarma": {"pais": "Peru"},
    "plazavea": {"pais": "Peru"},
    "avonper": {"pais": "Peru"},
    "avonecu": {"pais": "Ecuador"},
    "fybeca": {"pais": "Ecuador"},
    "tia": {"pais": "Ecuador"},
    "mercaliper": {"pais": "Peru"},
    "mercaliecu": {"pais": "Ecuador"},
    "naturacol": {"pais": "Colombia"},
    "naturaper": {"pais": "Peru"},
    "naturaecu": {"pais": "Ecuador"},
}

# Leer archivo de entrada
with open(input_file_path, "r") as input_file:
    reader = csv.DictReader(input_file)

    # CSV File Salida
    output_file_path = os.path.join(dest_folder, "resultado.csv")
    file_exists = os.path.exists(output_file_path)
    mode = "w+" if not file_exists else "a"

    with open(output_file_path, mode, newline="", encoding="ISO-8859-1") as output_file:
        # Encabezados
        fields = [
            "fecha",
            "sku",
            "pais",
            "fuente",
            "brand",
            "product_name",
            "precio_normal",
            "precio_descuento",
            "imagen",
        ]
        writer = csv.DictWriter(output_file, fieldnames=fields)
        if not file_exists:
            writer.writeheader()

        for linea in reader:
            if "fuente" not in linea:
                print("Linea Vacía")
                continue

            # Fuente Exito (OJO EN ALGUNOS CASOS APARECE RESULTADO PERO NO MUESTRA REUSLTADOS)
            if linea["fuente"] == "exito":
                print(
                    f"Procesando Archivo {linea['busqueda']} en la fuente {linea['fuente']}"
                )
                # Navigate to url
                # https://www.exito.com/speed%20stick?map=ft&page=2
                # https://www.exito.com/polvo%20compacto%20vogue?_q=polvo%20compacto%20vogue&map=ft
                driver.get(f"https://www.exito.com/{linea['busqueda']}?map=ft")

                # Esperar hasta que se tenga el total de botones cargados
                try:
                    WebDriverWait(driver, 20).until(
                        expected_conditions.visibility_of_all_elements_located(
                            (By.CLASS_NAME, "vtex-product-summary-2-x-imageNormal")
                        )
                    )
                except TimeoutException:
                    print("Se ha demorado mucho en cargar Inicial")
                # Scrapper

                time.sleep(5)
                total_productos = (
                    driver.find_element_by_class_name(
                        "vtex-search-result-3-x-totalProducts--layout"
                    )
                    .find_element_by_tag_name("span")
                    .text.split(" ")[0]
                )
                # print(total_productos)
                # linea daniel
                # print(total_productos)
                # linea daniel

                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")
                products = soup.find_all(
                    "div", class_="vtex-search-result-3-x-galleryItem"
                )
                has_results = True
                pagina = 1
                productos_acumulados = 0
                while has_results:

                    # Navegar a la pagina
                    print(f"Cargando Pagina {pagina}")
                    driver.get(
                        f"Https://www.exito.com/{linea['busqueda']}?map=ft&page={pagina}"
                    )

                    # Esperar hasta que se tenga el total de botones cargados
                    try:
                        WebDriverWait(driver, 60).until(
                            expected_conditions.visibility_of_all_elements_located(
                                (By.CLASS_NAME, "vtex-product-summary-2-x-imageNormal")
                            )
                        )
                    except TimeoutException:
                        print(f"Se ha demorado mucho en cargar la Pagina {pagina}")

                    tamano = 8000
                    posicion = 0
                    while posicion < tamano:
                        driver.execute_script(
                            "window.scrollTo({top:"
                            + str(posicion)
                            + ", left:0, behavior:'smooth'});"
                        )
                        posicion += tamano / 20
                        time.sleep(2)

                    html = driver.page_source
                    soup = BeautifulSoup(html, "html.parser")
                    products = soup.find_all(
                        "div", class_="vtex-search-result-3-x-galleryItem"
                    )
                    pagina += 1
                    productos_acumulados += len(products)
                    print(
                        f"Productos Acumulados: {productos_acumulados} de {total_productos}"
                    )
                    has_results = True if len(products) else False

                    for product in products:
                        # Listos
                        url_producto = urlparse(
                            product.find_all(
                                "a", class_="vtex-product-summary-2-x-clearLink"
                            )[0].attrs["href"]
                        )
                        params = parse_qs(url_producto.query)
                        if "skuId" in params.keys():
                            sku = params["skuId"][0]
                        else:
                            sku = product.find_all(
                                "div", class_="exito-product-details-3-x-elementScroll"
                            )[0].attrs["name"]
                        # Precio
                        high_price = product.find_all(
                            "div", class_="exito-vtex-components-4-x-list-price"
                        )
                        low_price = product.find_all(
                            "div",
                            class_="exito-vtex-components-4-x-selling-price",
                        )

                        if len(high_price):
                            high_price = high_price[0].text

                        if len(low_price):
                            low_price = low_price[0].text

                            if not len(high_price):
                                high_price = low_price
                        else:
                            low_price = "$ 0"

                        if not len(high_price):
                            high_price = low_price

                        # Imagen
                        picture = product.find_all(
                            "img", class_="vtex-product-summary-2-x-imageNormal"
                        )

                        product_name = product.find_all(
                            "span", class_="vtex-store-components-3-x-productBrand"
                        )

                        brand = product.find_all(
                            "span", class_="vtex-product-summary-2-x-productBrandName"
                        )

                        writer.writerow(
                            {
                                "fecha": datetime.datetime.now(),
                                "sku": sku,
                                "pais": fuentes[linea["fuente"]]["pais"],
                                "fuente": linea["fuente"].title(),
                                "brand": brand[0].text.strip().title(),
                                "product_name": product_name[0].text.strip().title(),
                                "precio_normal": "".join(
                                    caracter
                                    for caracter in high_price.strip()[1:].replace(
                                        ".", ""
                                    )
                                    if caracter.isprintable()
                                ),
                                "precio_descuento": "".join(
                                    caracter
                                    for caracter in low_price.strip()[1:].replace(
                                        ".", ""
                                    )
                                    if caracter.isprintable()
                                ).replace("Otros medios", ""),
                                "imagen": picture[0].attrs["src"],
                            }
                        )

            # Fuente Jumbo
            if linea["fuente"] == "jumbo":
                print(
                    f"Procesando Archivo {linea['busqueda']} en la fuente {linea['fuente']}"
                )
                # Navigate to url
                # https://www.tiendasjumbo.co/vogue%20polvo%20compacto%20natural?_q=VOGUE%20POLVO%20COMPACTO%20NATURAL&map=ft
                driver.get(
                    f"https://www.tiendasjumbo.co/{linea['busqueda']}?_q={linea['busqueda']}&map=ft"
                )

                # Esperar hasta que se tenga el total de botones cargados
                try:
                    WebDriverWait(driver, 20).until(
                        expected_conditions.visibility_of_all_elements_located(
                            (By.CLASS_NAME, "vtex-product-summary-2-x-imageNormal")
                        )
                    )
                except TimeoutException:
                    print("Se ha demorado mucho en cargar Inicial")

                # Scrapper
                try:
                    total_productos = int(
                        driver.find_element_by_class_name(
                            "vtex-search-result-3-x-totalProducts--layout"
                        ).text.split(" ")[0]
                    )

                except NoSuchElementException:
                    total_productos = 0
                    print("No se han encontrado resultados")
                    continue

                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")
                products = soup.find_all(
                    "div", class_="vtex-search-result-3-x-galleryItem"
                )

                # Cargar más productos
                productos_acumulados = 0
                while productos_acumulados < total_productos:
                    driver.execute_script(
                        "window.scrollTo({top:document.body.scrollHeight, left:0, behavior:'smooth'});"
                    )
                    time.sleep(2)
                    driver.execute_script(
                        "window.scrollTo({top:document.body.scrollHeight-1000, left:0, behavior:'smooth'});"
                    )

                    # clic al boton mostrar más
                    try:
                        driver.execute_script(
                            "document.querySelectorAll('a.vtex-button')[0].click()"
                        )
                    except JavascriptException:
                        pass

                    html = driver.page_source
                    soup = BeautifulSoup(html, "html.parser")
                    products = soup.find_all(
                        "div", class_="vtex-search-result-3-x-galleryItem"
                    )
                    productos_acumulados = len(products)
                    print(
                        f"Productos Acumulados: {productos_acumulados} de {total_productos}"
                    )

                for product in products:
                    # Imagen
                    picture = product.find_all("img")

                    # SKU
                    sku = (
                        product.find_all("input", class_="vtex-checkbox__input")[0]
                        .attrs["id"]
                        .split("-")[0]
                    )

                    # Precios
                    precios = product.find_all(
                        "div", class_="tiendasjumboqaio-jumbo-minicart-2-x-price"
                    )
                    if len(precios) > 1:
                        high_price = precios[0].text.replace(".", "")[2:]
                        low_price = precios[1].text.replace(".", "")[2:]
                    else:
                        high_price = low_price = precios[0].text.replace(".", "")[2:]

                    brand = product.find_all(
                        "span", class_="vtex-product-summary-2-x-productBrandName"
                    )[0].text

                    writer.writerow(
                        {
                            "fecha": datetime.datetime.now(),
                            "sku": sku,
                            "pais": fuentes[linea["fuente"]]["pais"],
                            "fuente": linea["fuente"].title(),
                            "brand": brand.title(),
                            "product_name": product.find_all(
                                "span", class_="vtex-product-summary-2-x-productBrand"
                            )[0].text,
                            "precio_normal": high_price,
                            "precio_descuento": low_price,
                            "imagen": picture[0].attrs["src"],
                        }
                    )

            # Fuente Farmatodo
            if linea["fuente"] == "farmatodo":
                print(
                    f"Procesando Archivo {linea['busqueda']} en la fuente {linea['fuente']}"
                )
                # Navigate to url
                # https://www.farmatodo.com.co/buscar?product=polvo%20compacto&departamento=Todos&filtros=
                driver.get(
                    f"https://www.farmatodo.com.co/buscar?product={linea['busqueda']}&departamento=Todos&filtros="
                )
                # Esperar hasta que se tenga el total de botones cargados

                try:
                    WebDriverWait(driver, 20).until(
                        expected_conditions.visibility_of_all_elements_located(
                            (By.TAG_NAME, "app-product-card")
                        )
                    )
                except TimeoutException:
                    print("Se ha demorado mucho en cargar Inicial")

                    # No tiene un totalizador de encuentro
                cargar_mas_button = True
                while cargar_mas_button:
                    try:
                        driver.execute_script(
                            "document.querySelector('#group-view-load-more').click()"
                        )
                    except:
                        cargar_mas_button = False
                    cargar_mas_button = not driver.find_element_by_id(
                        "group-view-load-more"
                    ).get_attribute("disabled")
                print("No se puede cargar más productos")
                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")
                products = soup.find_all("div", class_="add-information")

                for product in products:

                    # Imagen
                    picture = product.find_all("img", class_="image")

                    # SKU
                    sku = (
                        product.find_all("a", class_="product-image-link")[0]
                        .attrs["data-cuf"]
                        .encode("ISO-8859-1", "replace")
                        .decode("ISO-8859-1")
                    )
                    # Precios
                    low_price = product.find_all("span", class_="text-price")
                    high_price = product.find_all("span", class_="text-offer-price")
                    if len(high_price) > 0:
                        low_price = low_price[0].text[1:].replace(".", "")
                        high_price = high_price[0].text[1:].replace(".", "")
                    else:
                        low_price = low_price[0].text[1:].replace(".", "")
                        high_price = low_price

                    # Brand
                    brand = ""

                    # Nombre del producto
                    nombre_producto_ = (
                        product.find_all("div", class_="text-left")[0]
                        .text.replace("//", "")
                        .title()
                        .encode("ISO-8859-1", "replace")
                        .decode("ISO-8859-1")
                    )

                    writer.writerow(
                        {
                            "fecha": datetime.datetime.now(),
                            "sku": str(sku),
                            "pais": fuentes[linea["fuente"]]["pais"],
                            "fuente": linea["fuente"].title(),
                            "brand": brand.lower(),
                            "product_name": str(nombre_producto_),
                            "precio_normal": high_price,
                            "precio_descuento": low_price,
                            "imagen": picture[0].attrs["src"],
                        }
                    )

            # Wong https://www.wong.pe/busca/?ft=edred%C3%B3n
            if linea["fuente"] == "wong":

                print(
                    f"Procesando Archivo {linea['busqueda']} en la fuente {linea['fuente']}"
                )
                # Navigate to url
                driver.get(f"https://www.wong.pe/busca/?ft={linea['busqueda']}")

                # Esperar hasta que se tenga el total de botones cargados
                try:
                    WebDriverWait(driver, 20).until(
                        expected_conditions.visibility_of_all_elements_located(
                            (By.CLASS_NAME, "product-add-to-cart")
                        )
                    )
                except TimeoutException:
                    print("Se ha demorado mucho en cargar Inicial")
                # Scrapper
                total_productos = driver.find_element_by_class_name(
                    "amount"
                ).text.split(" ")[0]

                productos_acumulados = 0
                products = []
                # iterar hasta acumular el total de productos
                while productos_acumulados < int(total_productos):

                    # Hacer scroll hasta el final de la página
                    driver.execute_script(
                        "window.scrollTo({top:document.body.scrollHeight, left:0, behavior:'smooth'});"
                    )
                    time.sleep(5)

                    # Esperar hasta que se tenga el total de botones cargados
                    try:
                        WebDriverWait(driver, 30).until(
                            expected_conditions.visibility_of_all_elements_located(
                                (By.CLASS_NAME, "product-add-to-cart")
                            )
                        )
                    except TimeoutException:
                        pass

                    html = driver.page_source
                    soup = BeautifulSoup(html, "html.parser")
                    products = soup.find_all("div", class_="product-item")
                    productos_acumulados = len(products)
                    print(
                        f"Productos Acumulados: {productos_acumulados} de {total_productos}"
                    )

                for product in products:

                    # SKU
                    sku = product.attrs["data-sku"]

                    # Imagen
                    picture = product.find_all("img")[0].attrs["src"]

                    # Brand
                    brand = product.attrs["data-brand"]

                    # Nombre
                    name = product.attrs["data-name"]

                    # Precio
                    high_price = product.attrs["data-price"][3:]
                    low_price = product.find_all(
                        "span", class_="product-prices__value--best-price"
                    )
                    if len(low_price) == 0:
                        low_price = high_price
                    else:
                        low_price = low_price[0].text[2:]

                    writer.writerow(
                        {
                            "fecha": datetime.datetime.now(),
                            "sku": sku,
                            "pais": fuentes[linea["fuente"]]["pais"],
                            "fuente": linea["fuente"].title(),
                            "brand": brand.title(),
                            "product_name": name.title(),
                            "precio_normal": high_price,
                            "precio_descuento": low_price,
                            "imagen": picture,
                        }
                    )

            # MecardoLibre Col https://listado.mercadolibre.com.co/vogue-polvo-compacto_NoIndex_True
            # document.getElementsByClassName('andes-pagination__arrow-title')[1]
            if linea["fuente"] in ["mercalicol", "mercaliper", "mercaliecu"]:

                print(
                    f"Procesando Archivo {linea['busqueda']} en la fuente {linea['fuente']}"
                )
                # Navigate to url
                if linea["fuente"] == "mercalicol":
                    dominio = "co"
                elif linea["fuente"] == "mercaliper":
                    dominio = "pe"
                else:
                    dominio = "ec"

                driver.get(
                    f"https://listado.mercadolibre.com.{dominio}/{linea['busqueda']}_NoIndex_True"
                )

                # Esperar hasta que se tenga el total de botones cargados
                try:
                    WebDriverWait(driver, 20).until(
                        expected_conditions.visibility_of_all_elements_located(
                            (By.CLASS_NAME, "ui-search-layout__item")
                        )
                    )
                except TimeoutException:
                    print("Se ha demorado mucho en cargar Inicial")

                # Scrapper
                total_productos = int(
                    driver.find_element_by_class_name(
                        "ui-search-search-result__quantity-results"
                    )
                    .text.split(" ")[0]
                    .replace(".", "")
                )

                # print(criterio_pagina)
                productos_acumulados = 0
                contador_salto = 0
                products = []
                # iterar hasta acumular el total de productos
                while productos_acumulados < total_productos - contador_salto:

                    # Esperar hasta que se tenga el total de botones cargados
                    try:
                        WebDriverWait(driver, 30).until(
                            expected_conditions.visibility_of_all_elements_located(
                                (By.CLASS_NAME, "ui-search-layout__item")
                            )
                        )
                    except TimeoutException:
                        pass

                    html = driver.page_source
                    soup = BeautifulSoup(html, "html.parser")
                    products = soup.find_all("li", class_="ui-search-layout__item")
                    productos_acumulados += len(products)
                    print(
                        f"Productos Acumulados: {productos_acumulados} de {total_productos}"
                    )
                    time.sleep(5)

                    for product in products:

                        # Imagen

                        picture = product.find_all(
                            "img", class_="ui-search-result-image__element"
                        )[0].attrs["src"][:-4]

                        if not picture.startswith("https"):
                            picture = product.find_all(
                                "img", class_="ui-search-result-image__element"
                            )[0].attrs["data-src"][:-4]

                        # SKU
                        sku = re.search(r"(\d)*([MLA]|[MCO])+([0-9]*)", picture)

                        if sku:
                            sku = sku.group(3)
                        else:
                            sku = ""

                        # Brand
                        brand = ""

                        # Nombre
                        name = product.find_all("h2", class_="ui-search-item__title")[
                            0
                        ].text

                        # Precio
                        try:
                            low_price = product.find_all(
                                "div", class_="ui-search-price__second-line"
                            )[0].text.split(" ")[0]
                        except IndexError:
                            contador_salto += 1
                            continue  # para saltarlas

                        try:
                            high_price = product.find_all(
                                "s",
                                class_="price-tag ui-search-price__part ui-search-price__original-value price-tag__disabled",
                            )[0].text.split(" ")[1]
                        except:
                            high_price = low_price

                        writer.writerow(
                            {
                                "fecha": datetime.datetime.now(),
                                "sku": sku,
                                "pais": fuentes[linea["fuente"]]["pais"],
                                "fuente": linea["fuente"].title(),
                                "brand": brand,
                                "product_name": name.title(),
                                "precio_normal": high_price,
                                "precio_descuento": low_price,
                                "imagen": picture + "jpg",
                            }
                        )
                    # clic para siguiente
                    try:
                        driver.execute_script(
                            "document.getElementsByClassName('andes-pagination__button--next')[0].childNodes[0].click()"
                        )
                    except JavascriptException:
                        pass

            # Natura https://www.natura.com.co/s/productos?busca=%22labial%22

            if linea["fuente"] in ["naturacol", "naturaper"]:

                print(
                    f"Procesando Archivo {linea['busqueda']} en la fuente {linea['fuente']}"
                )
                # Navigate to url
                if linea["fuente"] == "naturacol":
                    dominio = "co"
                if linea["fuente"] == "naturaper":
                    dominio = "pe"

                driver.get(
                    # https://www.natura.com.co/s/productos?busca=%22labial%22
                    f"https://www.natura.com.{dominio}/s/productos?busca=%22{linea['busqueda']}%22"
                )

                # Esperar hasta que se tenga el total de botones cargados
                try:
                    WebDriverWait(driver, 20).until(
                        expected_conditions.visibility_of_all_elements_located(
                            (By.CSS_SELECTOR, "li[class^=ProductList_item]")
                        )
                    )
                except TimeoutException:
                    print("Se ha demorado mucho en cargar Inicial")

                # Scrapper

                productos_acumulados = 0
                products = []
                has_products = True
                # iterar hasta acumular el total de productos
                while has_products:

                    # Esperar hasta que se tenga el total de botones cargados
                    try:
                        WebDriverWait(driver, 20).until(
                            expected_conditions.visibility_of_all_elements_located(
                                (By.CSS_SELECTOR, "li[class^=ProductList_item]")
                            )
                        )
                    except TimeoutException:
                        pass

                    try:
                        driver.execute_script(
                            "document.querySelector('div[class^=\"ProductList_loadMore\"]').firstChild.click()"
                        )
                    except JavascriptException:
                        has_products = False
                        pass
                    time.sleep(2)

                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")
                products = soup.select("li[class^=ProductList_item]")
                total_productos = int(
                    re.sub(
                        "[^0-9]",
                        "",
                        soup.find_all(
                            "span", attrs={"data-testid": "search-title__total-results"}
                        )[0].text.split(" ")[0],
                    )
                )
                print(total_productos)
                # time.sleep(5)

                for product in products:

                    # Imagen
                    picture = product.find_all("img")[0].attrs["src"]

                    # SKU
                    sku = re.search(r"\/*([0-9]*)\/", picture).group(1)

                    # Brand
                    try:
                        brand = product.select(
                            "div:nth-child(1) >div:nth-child(1) >div:nth-child(2) >div:nth-child(1) >div:nth-child(1)"
                        )[0].text
                    except IndexError:
                        brand = ""

                    # Nombre
                    name = product.select(
                        "div:nth-child(1) >div:nth-child(1) >div:nth-child(2) >div:nth-child(1) >div:nth-child(2)"
                    )[0].text

                    # Precio
                    prices = product.select(
                        "div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1)"
                    )[0]
                    low_price = prices.find_all("div")[1].text

                    if low_price == "Indisponible":
                        continue

                    productos_acumulados += 1
                    print(
                        f"Productos Acumulados: {productos_acumulados} de {total_productos}"
                    )

                    low_price = low_price.split()[1].split("-")[0]

                    try:
                        high_price = prices.find_all("div")[0].text.split()[1]
                    except IndexError:
                        high_price = low_price

                    writer.writerow(
                        {
                            "fecha": datetime.datetime.now(),
                            "sku": sku,
                            "pais": fuentes[linea["fuente"]]["pais"],
                            "fuente": linea["fuente"].title(),
                            "brand": brand,
                            "product_name": name.title(),
                            "precio_normal": high_price,
                            "precio_descuento": low_price,
                            "imagen": picture,
                        }
                    )

            # Tia https://www.tia.com.ec/tinte%20har
            if linea["fuente"] == "tia":

                print(
                    f"Procesando Archivo {linea['busqueda']} en la fuente {linea['fuente']}"
                )
                # Navigate to url
                driver.get(f"https://www.tia.com.ec/{linea['busqueda']}")

                # Esperar hasta que se tenga el total de botones cargados
                try:
                    WebDriverWait(driver, 20).until(
                        expected_conditions.visibility_of_all_elements_located(
                            (By.CLASS_NAME, "btn-buy")
                        )
                    )
                except TimeoutException:
                    print("Se ha demorado mucho en cargar Inicial")
                # Scrapper
                total_productos = driver.find_element_by_id("totalProducts").text
                if not total_productos:
                    total_productos = driver.find_element_by_id("totalProducts2").text

                productos_acumulados = 0
                products = []
                # iterar hasta acumular el total de productos
                # TODO cambiar a si el boton desaparece o si end-pagination tiene offsetParent
                while productos_acumulados < int(total_productos):

                    # Hacer click en el botón de cargar más
                    try:
                        # Revisar este click, a veces parece que no funciona y lo que hace es un scroll
                        # driver.execute_script(
                        #     "document.getElementsByClassName('next-page')[0].click();"
                        # )
                        # Alternativa en Jquery
                        driver.execute_script("$('.next-page')[0].click()")

                        time.sleep(2)
                    except ElementNotInteractableException as error:
                        print("No se puede hacer click")
                        pass

                    # Esperar hasta que se tenga el total de botones cargados
                    try:
                        WebDriverWait(driver, 20).until(
                            expected_conditions.visibility_of_all_elements_located(
                                (By.CLASS_NAME, "btn-buy")
                            )
                        )
                    except TimeoutException:
                        pass

                    html = driver.page_source
                    soup = BeautifulSoup(html, "html.parser")
                    products = soup.find_all("li", class_="elem")
                    products = [
                        product for product in products if "layout" in product.attrs
                    ]
                    productos_acumulados = len(products)

                    fin_paginado = soup.find_all("div", class_="end-pagination")

                    print(
                        f"Productos Acumulados: {productos_acumulados} de {total_productos}"
                    )
                    if fin_paginado[0].attrs["style"] != "display:none;":
                        break

                for product in products:
                    # Imagen
                    picture = product.find_all("img")

                    # SKU
                    sku = product.find_all("input", class_="productid")

                    # Precio
                    high_price = product.find_all("span", class_="finalOldPrice")
                    low_price = product.find_all("span", class_="bestPrice")
                    if len(high_price) == 0:
                        high_price = low_price
                        if len(low_price) == 0:
                            continue
                    high_price = low_price

                    # Nombre Producto
                    product_name = product.find_all("span", class_="title")

                    # Marca
                    brand = product.find_all("a", class_="brand")

                    writer.writerow(
                        {
                            "fecha": datetime.datetime.now(),
                            "sku": sku[0].attrs["value"],
                            "pais": fuentes[linea["fuente"]]["pais"],
                            "fuente": linea["fuente"].title(),
                            "brand": brand[0].text,
                            "product_name": product_name[0].text.strip().title(),
                            "precio_normal": high_price[1].text.strip()[1:],
                            "precio_descuento": low_price[1].text.strip()[1:],
                            "imagen": picture[0].attrs["src"],
                        }
                    )
            # CAMBIO LA PÁGINA WEB
            # Fybeca https://www.fybeca.com/FybecaWeb/pages/search-results.jsf?cat=-1&q=roll+on&s=0&pp=25&ds=n
            #        https://www.fybeca.com/busqueda?q=desodorante+axe&search-button=&lang=es_EC
            #        https://www.fybeca.com/busqueda?q=pantene&search-button=&lang=es_EC

            if linea["fuente"] == "fybeca":
                print(
                    f"Procesando producto {linea['busqueda']} en la fuente {linea['fuente']}"
                )

                # Scrapper
                productos_acumulados = 0
                products = []
                has_products = True
                pagina = 0
                # iterar hasta acumular el total de productos
                while has_products:
                    # Navigate to url
                    driver.get(
                        f"https://www.fybeca.com/busqueda?q={linea['busqueda']}&&search-button=&lang=es_EC&start={pagina}&sz=18&maxsize=18"
                    )
                    # https://www.fybeca.com/busqueda?q=desodorante+axe&search-button=&lang=es_EC
                    # s={pagina}&pp=25&ds=n
                    # f"https://www.fybeca.com/FybecaWeb/pages/search-results.jsf?cat=-1&q={linea['busqueda']}&s={pagina}&pp=25&ds=n")
                    # https://www.fybeca.com/busqueda?q=ponds&search-button=&lang=es_EC

                    # Esperar hasta que se tenga el total de botones cargados
                    try:
                        print(f"Cargando pagina {int(pagina / 18)}")
                        WebDriverWait(driver, 20).until(
                            expected_conditions.visibility_of_all_elements_located(
                                (By.CLASS_NAME, "product-tile")
                            )
                        )
                    except TimeoutException:
                        print(f"Se ha demorado mucho en cargar pagina {int(pagina/18)}")

                    html = driver.page_source
                    soup = BeautifulSoup(html, "html.parser")
                    products = soup.find_all("div", class_="product")
                    # products = [product for product in products if "product" in product.attrs] Ya no hace falta esto era porque existía un elemento de paginador con el mismo nombre

                    has_products = len(products) > 0

                    print(
                        f"Productos en pagina {int(pagina/18)}: {len(products)}, Productos Acumulados: {productos_acumulados}"
                    )
                    productos_acumulados += len(products)

                    for product in products:

                        try:
                            product_id = product["data-pid"]
                        except KeyError:
                            continue

                        # SKU
                        sku = product.attrs["data-pid"][5:]

                        # Imagen
                        picture = product.find_all("img", class_="tile-image")

                        # Nombre
                        name = product.find_all("a", class_="link")[0].text.strip()

                        # Brand
                        brand = product.find_all("a", class_="product-brand")[
                            0
                        ].text.strip()

                        # Precio
                        high_price = product.find_all("span", class_="price-original")
                        low_price = product.find_all("span", class_="value pr-2")

                        if len(low_price) == 0:
                            low_price = high_price

                        # low_price = json.loads(product["data-price"])["vitalcard"]

                        writer.writerow(
                            {
                                "fecha": datetime.datetime.now(),
                                "sku": sku,
                                "pais": fuentes[linea["fuente"]]["pais"],
                                "fuente": linea["fuente"].title(),
                                "brand": brand,
                                "product_name": name.title(),
                                "precio_normal": high_price[0]
                                .text.strip()
                                .strip("$")[:-8]
                                .strip(),
                                "precio_descuento": low_price[0]
                                .text.strip()
                                .strip("$"),
                                "imagen": picture[0].attrs["src"],
                            }
                        )
                    # Incrementar item de inicio siguiente pagina.
                    pagina += 18

            # Inkafarma https://inkafarma.pe/buscador?keyword=nivea
            if linea["fuente"] == "inkafarma":
                print(
                    f"Procesando Archivo {linea['busqueda']} en la fuente {linea['fuente']}"
                )

                # Navigate to url Inkafarma
                driver.get(f"https://inkafarma.pe/buscador?keyword={linea['busqueda']}")

                # Esperar hasta que se tenga el total de botones cargados
                try:
                    WebDriverWait(driver, 20).until(
                        expected_conditions.visibility_of_all_elements_located(
                            (By.TAG_NAME, "fp-product-large")
                        )
                    )
                except TimeoutException:
                    print("Se ha demorado mucho en cargar Inicial")
                # Scrapper
                try:
                    total_productos = int(
                        driver.find_element_by_css_selector("h3").text.split(" ")[1]
                    )
                except NoSuchElementException:
                    total_productos = 0
                    print("No se han encontrado resultados")
                    continue

                # Cargar más productos
                productos_acumulados = productos_previos = 0
                products = []
                productos_previos = 0
                reintentos = 0
                while productos_acumulados < total_productos and reintentos < 7:
                    driver.execute_script(
                        "window.scrollTo({top:document.body.scrollHeight, left:0, behavior:'smooth'});"
                    )
                    time.sleep(2)
                    driver.execute_script(
                        "window.scrollTo({top:document.body.scrollHeight-1000, left:0, behavior:'smooth'});"
                    )

                    html = driver.page_source
                    soup = BeautifulSoup(html, "html.parser")
                    products = soup.find_all("fp-product-large")
                    productos_acumulados = len(products)
                    if productos_acumulados == productos_previos:
                        reintentos += 1
                    productos_previos = productos_acumulados
                    print(
                        f"Productos Acumulados: {productos_acumulados} de {total_productos}"
                    )

                for product in products:
                    # Imagen
                    picture = product.find_all("img")

                    # SKU
                    sku = product.find_all("a", class_="link")

                    # Precio
                    low_price = product.find_all("fp-product-price")
                    high_price = product.find_all("fp-product-regular-price")

                    if len(low_price) == 0:
                        continue

                    writer.writerow(
                        {
                            "fecha": datetime.datetime.now(),
                            "sku": re.search(r"[0-9]+$", sku[0].attrs["href"])[0],
                            "pais": fuentes[linea["fuente"]]["pais"],
                            "fuente": linea["fuente"].title(),
                            "brand": "",
                            "product_name": picture[0].attrs["alt"].title(),
                            "precio_normal": high_price[0].attrs[
                                "ng-reflect-regular-price"
                            ]
                            if len(high_price)
                            else low_price[0].attrs["ng-reflect-price"],
                            "precio_descuento": low_price[0].attrs["ng-reflect-price"],
                            "imagen": picture[0].attrs["src"],
                        }
                    )

            # plazavea https://www.plazavea.com.pe/search/?_query=desodorante
            # IMPORTANTE EN EL CASO DE DESODORANTE LLEGO A 214 DE 244 Y SE QUEDO INTENTANDO CAPTURAR MÁS SIN LOGRARLO. CAMBIÉ EL CRÍTERIO DEL WHILE POR INTENTOS. SIN EMBARGO, SÓLO CAPTURA 19 REGISTROS.
            if linea["fuente"] == "plazavea":
                print(
                    f"Procesando Archivo {linea['busqueda']} en la fuente {linea['fuente']}"
                )

                # Navigate to url Inkafarma
                driver.get(
                    f"https://www.plazavea.com.pe/search/?_query={linea['busqueda']}"
                )

                # Esperar hasta que se tenga el total de botones cargados
                try:
                    WebDriverWait(driver, 20).until(
                        expected_conditions.visibility_of_all_elements_located(
                            (By.CLASS_NAME, "HA Showcase")
                            # document.getElementsByClassName("HA Showcase") así a través de consola se valida la cantidad de elementos hallados.
                        )
                    )
                except TimeoutException:
                    print("Se ha demorado mucho en cargar Inicial")
                # Scrapper
                try:
                    total_productos = int(
                        driver.find_element_by_css_selector(
                            ".Search__content__count__total"
                        ).text
                    )
                except NoSuchElementException:
                    total_productos = 0
                    print("No se han encontrado resultados")
                    continue

                # Cargar más productos
                productos_acumulados = productos_previos = 0
                products = []
                conteo_plazavea = 0

                while conteo_plazavea < 1:  #
                    # while productos_acumulados < total_productos:

                    driver.execute_script(
                        'document.querySelector("div.Search__content__nav > div > ul > li:nth-child(4)").click()'
                    )

                    for scroll in range(0, 5):
                        driver.execute_script(
                            "window.scrollTo({top:document.body.scrollHeight, left:0, behavior:'smooth'});"
                        )
                        time.sleep(1)
                        driver.execute_script(
                            "window.scrollTo({top:document.body.scrollHeight-1500, left:0, behavior:'smooth'});"
                        )
                        time.sleep(3)

                    html = driver.page_source
                    soup = BeautifulSoup(html, "html.parser")
                    products = soup.find_all("div", class_="Showcase")
                    productos_previos = productos_acumulados  #
                    productos_acumulados = len(products)  #
                    # print(productos_previos, productos_acumulados, conteo_plazavea) #
                    print(
                        f"Productos Acumulados: {productos_acumulados} de {total_productos}"
                    )
                    # if productos_previos == productos_acumulados: #
                    conteo_plazavea += 1  #
                    # print(conteo_plazavea) #

                for product in products:
                    # Imagen
                    picture = product.find_all("img")

                    # SKU
                    sku = product.attrs["data-sku"]

                    # Precio regular
                    high_price = product.find_all("div", class_="Showcase__oldPrice")

                    # Precio oferta
                    low_price = product.find_all("div", class_="Showcase__salePrice")

                    brand = product.find_all("a", class_="brand")[0].text

                    product_name = product.find_all("div", class_="Showcase__content")[
                        0
                    ].attrs["title"]

                    if len(high_price) == 0:
                        high_price = low_price

                    writer.writerow(
                        {
                            "fecha": datetime.datetime.now(),
                            "sku": sku,
                            "pais": fuentes[linea["fuente"]]["pais"],
                            "fuente": linea["fuente"].title(),
                            "brand": brand,
                            "product_name": product_name,
                            "precio_normal": high_price[0].text.split(" ")[1],
                            "precio_descuento": low_price[0].text.split(" ")[1],
                            "imagen": picture[0].attrs["src"],
                        }
                    )

            # PROBLEMA CON COLOR TREND DESPUÉS DE LOS 46 DE 173 REGISTROS ERROR  "812 UNICODE"
            # avoncol https://www.avon.co/search/results/?q=FAR%20AWAY%20EAU
            if linea["fuente"] == "avoncol":
                print(
                    f"Procesando producto {linea['busqueda']} en la fuente {linea['fuente']}"
                )

                # Navigate to url avoncol
                driver.get(f"https://www.avon.co/search/results/?q={linea['busqueda']}")

                # Esperar hasta que se tenga el total de botones cargados
                try:
                    WebDriverWait(driver, 30).until(
                        expected_conditions.presence_of_all_elements_located(
                            (By.CLASS_NAME, "ProductListCell")
                        )
                    )
                except TimeoutException:
                    print("Se ha demorado mucho en carga Inicial")
                time.sleep(4)

                # Scrapper
                try:
                    total_productos = int(
                        driver.find_element_by_css_selector(
                            "strong.ng-binding:nth-child(1)"
                        ).text
                    )

                except NoSuchElementException:
                    total_productos = 0
                    print("No se han encontrado resultados")
                    continue

                # print(f"Cantidad de Productos Selenium: {len(driver.find_elements_by_class_name('ProductListCell'))}")
                # Cargar productos
                productos_acumulados = 0
                products = []

                # Determinar numero de paginas

                paginas = math.ceil(total_productos / 20)
                # print(f"Productos encontrados: {total_productos}")

                time.sleep(5)
                driver.execute_script(
                    "window.scrollTo({top:document.body.scrollHeight, left:0, behavior:'smooth'});"
                )

                # Cargar productos pagina a pagina
                for pagina in range(1, paginas + 1):
                    # Navegar a la pagina
                    print(f"Cargando Pagina {pagina}")
                    driver.get(
                        f"https://www.avon.co/search/results/?q={linea['busqueda']}#page={pagina}"
                    )

                    # Esperar hasta que se tenga el total de botones cargados
                    try:
                        WebDriverWait(driver, 30).until(
                            expected_conditions.presence_of_all_elements_located(
                                (By.CLASS_NAME, "ProductListCell")
                            )
                        )
                    except TimeoutException:
                        print(f"Ha tardado la carga de la pagina {pagina}")

                    time.sleep(4)
                    html = None
                    html = driver.page_source
                    soup = BeautifulSoup(html, "html.parser")
                    products = soup.find_all("div", class_="ProductListCell")
                    productos_acumulados += len(products)
                    print(
                        f"Productos Acumulados: {productos_acumulados} de {total_productos}"
                    )

                    for product in products:

                        # Imagen
                        picture = product.find_all("img")

                        # SKU
                        sku = picture[0].attrs["data-src"].split("_")[1]

                        # Precio regular
                        high_price = product.select(
                            "div.ListPrice.ng-scope span.ng-binding"
                        )

                        # Precio oferta
                        low_price = product.find_all(
                            "div", class_="Price ng-binding PriceDiscount"
                        )

                        if len(low_price):
                            low_price = low_price[0].text
                        else:
                            low_price = product.find_all(
                                "div", class_="Price ng-binding PriceList"
                            )
                            if len(low_price):
                                low_price = low_price[0].text
                            else:
                                low_price = "$0.0"

                        if len(high_price):
                            high_price = high_price[0].text
                        else:
                            high_price = low_price

                        # Para saber si los elementos están agotados
                        # is_available = len(product.find_all("div", class_="Availabilityng-scope"))

                        brand = ""

                        product_name = product.find_all("a", class_="ProductName")[
                            0
                        ].text

                        writer.writerow(
                            {
                                "fecha": datetime.datetime.now(),
                                "sku": sku,
                                "pais": fuentes[linea["fuente"]]["pais"],
                                "fuente": linea["fuente"].title(),
                                "brand": brand,
                                "product_name": unicodedata.normalize(
                                    "NFKD", product_name
                                )
                                .encode("ascii", "ignore")
                                .decode("utf-8"),
                                "precio_normal": "".join(
                                    caracter
                                    for caracter in high_price.strip()[1:].replace(
                                        ".", ""
                                    )
                                    if caracter.isprintable()
                                ),
                                "precio_descuento": "".join(
                                    caracter
                                    for caracter in low_price.strip()[1:].replace(
                                        ".", ""
                                    )
                                    if caracter.isprintable()
                                ),
                                "imagen": picture[0].attrs["data-src"],
                            }
                        )
                print(
                    f"Productos Acumulados: {productos_acumulados} de {total_productos}"
                )

            # avonper https://www.avon.com.pe/search/results/?q=far%20away%20eua
            if linea["fuente"] == "avonper":
                print(
                    f"Procesando producto {linea['busqueda']} en la fuente {linea['fuente']}"
                )

                # Navigate to url avonper
                driver.get(
                    f"https://www.avon.com.pe/search/results/?q={linea['busqueda']}"
                )

                # Esperar hasta que se tenga el total de botones cargados
                try:
                    WebDriverWait(driver, 30).until(
                        expected_conditions.presence_of_all_elements_located(
                            (By.CLASS_NAME, "ProductListCell")
                        )
                    )
                except TimeoutException:
                    print("Se ha demorado mucho en carga Inicial")
                time.sleep(4)

                # Scrapper
                try:
                    total_productos = int(
                        driver.find_element_by_css_selector(
                            "strong.ng-binding:nth-child(1)"
                        ).text
                    )
                except NoSuchElementException:
                    total_productos = 0
                    print("No se han encontrado resultados")
                    continue

                print(
                    f"Cantidad de Productos Selenium: {len(driver.find_elements_by_class_name('ProductListCell'))}"
                )
                # Cargar productos
                productos_acumulados = 0
                products = []

                # Determinar numero de paginas

                paginas = math.ceil(total_productos / 20)
                print(f"Productos encontrados: {total_productos}")

                # Cargar productos pagina a pagina
                for pagina in range(1, paginas + 1):
                    # Navegar a la pagina
                    print(f"Cargando Pagina {pagina}")
                    driver.get(
                        f"https://www.avon.com.pe/search/results/?q={linea['busqueda']}#page={pagina}"
                    )

                    # Esperar hasta que se tenga el total de botones cargados
                    try:
                        WebDriverWait(driver, 30).until(
                            expected_conditions.presence_of_all_elements_located(
                                (By.CLASS_NAME, "ProductListCell")
                            )
                        )
                    except TimeoutException:
                        print(f"Ha tardado la carga de la pagina {pagina}")

                    time.sleep(4)
                    html = None
                    html = driver.page_source
                    soup = BeautifulSoup(html, "html.parser")
                    products = soup.find_all("div", class_="ProductListCell")
                    productos_acumulados += len(products)
                    print(
                        f"Productos Acumulados: {productos_acumulados} de {total_productos}"
                    )

                    for product in products:

                        # Imagen
                        picture = product.find_all("img")

                        # SKU
                        sku = picture[0].attrs["data-src"].split("_")[1]

                        # Precio regular
                        high_price = product.select(
                            "div.ListPrice.ng-scope span.ng-binding"
                        )

                        # Precio oferta
                        low_price = product.find_all(
                            "div", class_="Price ng-binding PriceDiscount"
                        )

                        if len(low_price):
                            low_price = low_price[0].text
                        else:
                            low_price = "S/.0.0"

                        if len(high_price):
                            high_price = high_price[0].text
                        else:
                            high_price = low_price

                        # Para saber si los elementos están agotados
                        # is_available = len(product.find_all("div", class_="Availabilityng-scope"))

                        brand = ""

                        product_name = product.find_all("a", class_="ProductName")[
                            0
                        ].text

                        writer.writerow(
                            {
                                "fecha": datetime.datetime.now(),
                                "sku": sku,
                                "pais": fuentes[linea["fuente"]]["pais"],
                                "fuente": linea["fuente"].title(),
                                "brand": brand,
                                "product_name": unicodedata.normalize(
                                    "NFKD", product_name
                                )
                                .encode("ascii", "ignore")
                                .decode("utf-8"),
                                "precio_normal": "".join(
                                    caracter
                                    for caracter in high_price.strip()[0:].replace(
                                        "S/.", ""
                                    )
                                    if caracter.isprintable()
                                ),
                                "precio_descuento": "".join(
                                    caracter
                                    for caracter in low_price.strip()[0:].replace(
                                        "S/.", ""
                                    )
                                    if caracter.isprintable()
                                ),
                                "imagen": picture[0].attrs["data-src"],
                            }
                        )
                print(
                    f"Productos Acumulados: {productos_acumulados} de {total_productos}"
                )

            # avonecu https://www.avon.com.ec/search/results/?q=far%20away%20eua
            if linea["fuente"] == "avonecu":
                print(
                    f"Procesando producto {linea['busqueda']} en la fuente {linea['fuente']}"
                )

                # Navigate to url avonecu
                driver.get(
                    f"https://www.avon.com.ec/search/results/?q={linea['busqueda']}"
                )

                # Esperar hasta que se tenga el total de botones cargados
                try:
                    WebDriverWait(driver, 30).until(
                        expected_conditions.presence_of_all_elements_located(
                            (By.CLASS_NAME, "ProductListCell")
                        )
                    )
                except TimeoutException:
                    print("Se ha demorado mucho en carga Inicial")
                time.sleep(4)

                # Scrapper
                try:
                    total_productos = int(
                        driver.find_element_by_css_selector(
                            "strong.ng-binding:nth-child(1)"
                        ).text
                    )
                except NoSuchElementException:
                    total_productos = 0
                    print("No se han encontrado resultados")
                    continue

                print(
                    f"Cantidad de Productos Selenium: {len(driver.find_elements_by_class_name('ProductListCell'))}"
                )
                # Cargar productos
                productos_acumulados = 0
                products = []

                # Determinar numero de paginas

                paginas = math.ceil(total_productos / 20)
                print(f"Productos encontrados: {total_productos}")

                # Cargar productos pagina a pagina
                for pagina in range(1, paginas + 1):
                    # Navegar a la pagina
                    print(f"Cargando Pagina {pagina}")
                    driver.get(
                        f"https://www.avon.com.ec/search/results/?q={linea['busqueda']}#page={pagina}"
                    )

                    # Esperar hasta que se tenga el total de botones cargados
                    try:
                        WebDriverWait(driver, 30).until(
                            expected_conditions.presence_of_all_elements_located(
                                (By.CLASS_NAME, "ProductListCell")
                            )
                        )
                    except TimeoutException:
                        print(f"Ha tardado la carga de la pagina {pagina}")

                    time.sleep(4)
                    html = None
                    html = driver.page_source
                    soup = BeautifulSoup(html, "html.parser")
                    products = soup.find_all("div", class_="ProductListCell")
                    productos_acumulados += len(products)
                    print(
                        f"Productos Acumulados: {productos_acumulados} de {total_productos}"
                    )

                    for product in products:

                        # Imagen
                        picture = product.find_all("img")

                        # SKU
                        sku = picture[0].attrs["data-src"].split("_")[1]

                        # Precio regular
                        high_price = product.select(
                            "div.ListPrice.ng-scope span.ng-binding"
                        )

                        # Precio oferta
                        low_price = product.find_all(
                            "div", class_="Price ng-binding PriceDiscount"
                        )

                        if len(low_price):
                            low_price = low_price[0].text
                        else:
                            low_price = "$0.0"

                        if len(high_price):
                            high_price = high_price[0].text
                        else:
                            high_price = low_price

                        # Para saber si los elementos están agotados
                        # is_available = len(product.find_all("div", class_="Availabilityng-scope"))

                        brand = ""

                        product_name = product.find_all("a", class_="ProductName")[
                            0
                        ].text

                        writer.writerow(
                            {
                                "fecha": datetime.datetime.now(),
                                "sku": sku,
                                "pais": fuentes[linea["fuente"]]["pais"],
                                "fuente": linea["fuente"].title(),
                                "brand": brand,
                                "product_name": unicodedata.normalize(
                                    "NFKD", product_name
                                )
                                .encode("ascii", "ignore")
                                .decode("utf-8"),
                                "precio_normal": "".join(
                                    caracter
                                    for caracter in high_price.strip()[1:].replace(
                                        ".", ""
                                    )
                                    if caracter.isprintable()
                                ),
                                "precio_descuento": "".join(
                                    caracter
                                    for caracter in low_price.strip()[1:].replace(
                                        ".", ""
                                    )
                                    if caracter.isprintable()
                                ),
                                "imagen": picture[0].attrs["data-src"],
                            }
                        )
                print(
                    f"Productos Acumulados: {productos_acumulados} de {total_productos}"
                )

            # Fuente D1
            if linea["fuente"] == "D1":
                print(
                    f"Procesando Archivo {linea['busqueda']} en la fuente {linea['fuente']}"
                )
                # Navigate to url
                driver.get(f"https://domicilios.tiendasd1.com")
                time.sleep(2)
                driver.get(
                    f"https://domicilios.tiendasd1.com/search?name={linea['busqueda']}"
                )

                # https://domicilios.tiendasd1.com/search?name=FRAGANCIA

                # Esperar hasta que se tenga el total de botones cargados
                try:
                    WebDriverWait(driver, 20).until(
                        expected_conditions.visibility_of_all_elements_located(
                            (By.CLASS_NAME, "prod--default__content")
                        )
                    )
                except TimeoutException:
                    print("Se ha demorado mucho en cargar Inicial")
                # Scrapper
                total_productos = (
                    driver.find_element_by_class_name("category-text")
                    .find_element_by_tag_name("p")
                    .text.split(" ")[0]
                )
                # linea daniel
                # print(total_productos)
                # linea daniel

                # encontrar boton siguiente
                #   html = driver.page_source
                #   soup = BeautifulSoup(html, "html.parser")
                #   products = soup.find_all(
                #      "div", class_="prod--default"
                #   )
                has_results = True
                pagina = 1
                productos_acumulados = 0
                if total_productos == "resultados":
                    total_productos = 0

                while productos_acumulados < int(total_productos):
                    time.sleep(3)
                    html = driver.page_source
                    soup = BeautifulSoup(html, "html.parser")
                    products = soup.find_all("div", class_="prod--default")

                    # Navegar a la pagina
                    print(f"Cargando Pagina {pagina}")

                    pagina += 1
                    productos_acumulados += len(products)
                    has_results = True if len(products) else False

                    for product in products:
                        # Listos
                        #   print(product.find_all(
                        #    "img", class_="prod__image__img"
                        #   )[0].attrs['src'].split("/")[-1].split(".")[0])
                        sku = product.find_all("img")[0].attrs["src"]
                        sku = sku.split("/")[-1].split(".")[0]

                        # Precio
                        high_price = product.find_all(
                            "p", class_="prod--default__price__current"
                        )
                        low_price = product.find_all(
                            "p",
                            class_="prod--default__price__special-off",
                        )
                        if low_price[0].text == "":
                            low_price = high_price

                        if len(high_price) == 0:
                            high_price = low_price

                        # Imagen
                        picture = product.find_all("img", class_="prod__image__img")

                        product_name = picture[0].attrs["alt"]

                        writer.writerow(
                            {
                                "fecha": datetime.datetime.now(),
                                "sku": sku,
                                "pais": fuentes[linea["fuente"]]["pais"],
                                "fuente": linea["fuente"].title(),
                                "brand": "",
                                "product_name": product_name.strip().title(),
                                "precio_normal": "".join(
                                    caracter
                                    for caracter in high_price[0]
                                    .text.strip()[1:]
                                    .replace(".", "")
                                    if caracter.isprintable()
                                ),
                                "precio_descuento": "".join(
                                    caracter
                                    for caracter in low_price[0]
                                    .text.strip()[1:]
                                    .replace(".", "")
                                    if caracter.isprintable()
                                ),
                                "imagen": picture[0].attrs["src"],
                            }
                        )

            # Fuente ARA
            if linea["fuente"] == "ARA":
                print(
                    f"Procesando Archivo {linea['busqueda']} en la fuente {linea['fuente']}"
                )
                # Navigate to url
                driver.get(f"https://domicilios.aratiendas.com/")

                driver.execute_script(
                    "document.getElementsByClassName('v-select__slot')[0].click()"
                )
                driver.execute_script(
                    "document.getElementsByClassName('v-select-list')[0].querySelectorAll('div')[0].click()"
                )
                driver.execute_script(
                    "document.getElementsByName('address')[0].value='Calle 66 No. 50 - 84'"
                )
                driver.execute_script(
                    "document.getElementsByName('address')[0].dispatchEvent(new Event('input'))"
                )
                driver.execute_script(
                    "document.getElementsByClassName('search-desktop')[0].click()"
                )
                time.sleep(2)
                driver.execute_script(
                    "document.getElementsByClassName('continue v-btn')[0].click()"
                )
                time.sleep(2)
                driver.execute_script(
                    "document.getElementsByClassName('v-input__control')[0].querySelectorAll('input')[0].value='"
                    + linea["busqueda"]
                    + "'"
                )
                driver.execute_script(
                    "document.getElementsByClassName('v-input__control')[0].querySelectorAll('input')[0].dispatchEvent(new Event('input'))"
                )
                driver.execute_script(
                    "document.getElementsByClassName('all-products-btn')[0].click()"
                )

                # Hacer Scroll hasta el final de la página
                time.sleep(5)
                driver.execute_script(
                    "window.scrollTo({top:document.body.scrollHeight, left:0, behavior:'smooth'});"
                )
                time.sleep(5)
                driver.execute_script(
                    "window.scrollTo({top:0, left:0, behavior:'smooth'});"
                )
                # Esperar hasta que se tenga el total de botones cargados
                try:
                    WebDriverWait(driver, 30).until(
                        expected_conditions.visibility_of_all_elements_located(
                            (By.CLASS_NAME, "v-image__image--contain")
                        )
                    )
                except TimeoutException:
                    print("Se ha demorado mucho en cargar Inicial_")
                # Scrapper
                total_productos = int(
                    driver.find_element_by_class_name("picked-title")
                    .text.strip()
                    .split(" ")[0]
                )

                has_results = True
                pagina = 1
                productos_acumulados = 0

                while productos_acumulados < total_productos - 1:
                    time.sleep(3)
                    try:
                        WebDriverWait(driver, 40).until(
                            expected_conditions.visibility_of_all_elements_located(
                                (By.CLASS_NAME, "v-image__image--contain")
                            )
                        )
                    except TimeoutException:
                        print("Se ha demorado mucho en cargar Inicial__")
                    html = None
                    html = driver.page_source
                    soup = BeautifulSoup(html, "html.parser")
                    products = None
                    products = soup.find_all("div", class_="product-category")

                    pagina += 1
                    productos_acumulados += len(products)
                    has_results = True if len(products) else False

                    for index, product in enumerate(products):

                        # Precio
                        high_price = product.find_all("h2", class_="price")
                        low_price = product.find_all(
                            "h2",
                            class_="price",
                        )

                        # Imagen
                        try:
                            picture = product.find_all(
                                "div", class_="v-image__image--contain"
                            )[0]["style"].split('"')[1]
                        except:
                            picture = ""

                        # SKU
                        sku = re.search(r"[-]+(\d*)[-]*", picture).group(1)

                        product_name = product.find_all("span", class_="name_product")
                        writer.writerow(
                            {
                                "fecha": datetime.datetime.now(),
                                "sku": sku,
                                "pais": fuentes[linea["fuente"]]["pais"],
                                "fuente": linea["fuente"].title(),
                                "brand": "",
                                "product_name": product_name[0].text.strip().title(),
                                "precio_normal": "".join(
                                    caracter
                                    for caracter in high_price[0]
                                    .text.strip()[1:]
                                    .replace(".", "")
                                    if caracter.isprintable()
                                ),
                                "precio_descuento": "".join(
                                    caracter
                                    for caracter in low_price[0]
                                    .text.strip()[1:]
                                    .replace(".", "")
                                    if caracter.isprintable()
                                ),
                                "imagen": picture,
                            }
                        )
                    print(
                        f"Productos Acumulados: {productos_acumulados} de {total_productos}"
                    )

                    try:
                        print("cargando pagina")
                        driver.execute_script(
                            "document.querySelectorAll('[aria-label=\"Next page\"]')[0].click()"
                        )
                        time.sleep(2)
                    except JavascriptException:
                        print("No hay más páginas")
    driver.quit()
    print("Proceso terminado")
