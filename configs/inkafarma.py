from scrappers.base import BaseScrapper
from structures.products import InkafarmaProduct

config = {
        "pais": "Peru",
        "fuente": "Inkafarma.com",
        "scrapper_class": BaseScrapper,
        "url": "https://inkafarma.pe/buscador?keyword=nivea",
        "product_class": InkafarmaProduct,
        "search_placeholder": "nivea",
        "product_selector": "fp-product-large.ng-star-inserted",
        "product_count_selector": "h3.m-0 heading-3",
        "stop_behavior": BaseScrapper.STOP_IF_PRODUCT_COUNT_REACHED,
        "page_type": BaseScrapper.SINGLE_PAGE,
        "sku_selector": "a.link",
        "brand_selector": "",
        "product_name_selector": "img",
        "regular_price_selector": "fp-product-regular-price",
        "discount_price_selector": "fp-product-price",
        "image_selector": "img",
        "do_scroll": True,
        "browser": BaseScrapper.USE_CHROME,
        "show_browser": True,
        "verbose": True,
    }