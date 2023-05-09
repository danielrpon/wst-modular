from scrappers.base import D1Scrapper, BaseScrapper
from structures.products import D1Product

# TODO FUNCIONA pero está pendiente obtener la marca (se encuentra dentro de Modal)
config = {
    "pais": "Colombia",
    "scrapper_class": D1Scrapper,
    "product_class": D1Product,
    "fuente": "D1.com",
    "url": "https://domicilios.tiendasd1.com/search?name=placeholder",
    "search_placeholder": "placeholder",
    "product_selector": "div.card-product-vertical",
    "stop_behavior": BaseScrapper.STOP_IF_PAGE_COUNT_REACHED,
    "page_type": BaseScrapper.SSR_PAGE,
    "sku_selector": "img.prod__figure__img",
    "product_name_selector": "img.prod__figure__img",
    "regular_price_selector": "p.base__price",
    "discount_price_selector": "p.base__price",
    "image_selector": "img.prod__figure__img",
    "do_scroll": True,
    "browser": BaseScrapper.USE_CHROME,
    "show_browser": True,
    "verbose": True,
}