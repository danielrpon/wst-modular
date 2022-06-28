from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from scrappers.base import BaseScrapper

# Lectura del archivo de entrada
configuraciones = [
    {
        "pais": "Colombia",
        "fuente": "Exito.com",
        "url": "https://www.exito.com/guaro?_q=guaro&map=ft&page=pagenum",
        "search_placeholder": "guaro",
        "page_placeholder": "pagenum",
        "product_selector": "div.vtex-search-result-3-x-galleryItem",
        "product_count_selector": ".vtex-search-result-3-x-totalProducts--layout > span:nth-child(1)",
        "stop_behavior": BaseScrapper.STOP_IF_NO_PRODUCTS,
        "pagination_selector": ".min-h-small",
        "sku_selector": "div.exito-product-details-3-x-elementScroll",
        "brand_selector": "span.vtex-product-summary-2-x-productBrandName",
        "product_name_selector": "span.vtex-store-components-3-x-productBrand",
        "regular_price_selector": "div.exito-vtex-components-4-x-PricePDP",
        "discount_price_selector": "div.exito-vtex-components-4-x-list-price",
        "image_selector": "img.vtex-product-summary-2-x-image",
        "do_scroll": True,
    }
]
# Instanciar un scrapper (por fuente)
scrapper = BaseScrapper(**configuraciones[0])

for index, product in enumerate(scrapper.get_products("desodorante rexona")):
    print(product.sku, product.product_name)
    # Escribir to CSV
