from scrappers.base import ZaraScrapper, BaseScrapper
from structures.products import ZaraProduct

# TODO FUNCIONA pero está pendiente obtener la marca (se encuentra dentro de Modal)
config = {
    "pais": "Argentina",
    "scrapper_class": ZaraScrapper,
    "product_class": ZaraProduct,
    "fuente": "zara.com",
    "url": "https://www.zara.com/ar/es/mujer-prendas-exterior-l1184.html?v1=2041216",
    "search_placeholder": "mujer-prendas-exterior-l1184",
    "product_selector": "li.product-grid-product",
    "stop_behavior": BaseScrapper.STOP_IF_PRODUCT_COUNT_REACHED,
    "page_type": BaseScrapper.SINGLE_PAGE,
    "sku_selector": "li.product-grid-product",

    "product_name_selector": "img.media-image__image",
    "regular_price_selector": "span.money-amount__main",
    "discount_price_selector": "span.money-amount__main",

    "image_selector": "img.media-image__image",
    "do_scroll": True,
    "browser": BaseScrapper.USE_CHROME,
    "show_browser": True,
    "verbose": True,
}