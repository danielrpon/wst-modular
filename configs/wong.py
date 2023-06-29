from scrappers.base import BaseScrapper
from structures.products import WongProduct

config = {
        "pais": "Peru",
        "fuente": "wong.pe/",
        "scrapper_class": BaseScrapper,
        "url": "https://www.wong.pe/pantene?_q=pantene&map=ft",
        "product_class":  WongProduct,
        "search_placeholder": "pantene",
        "product_selector": "div.vtex-search-result-3-x-galleryItem",
        "product_count_selector": "div.vtex-search-result-3-x-totalProducts--layout",
        "stop_behavior": BaseScrapper.STOP_IF_SELECTOR_NOT_PRESENT,
        "page_type": BaseScrapper.SINGLE_PAGE,
        "pagination_selector": "vtex-search-result-3-x-buttonShowMore",
        "sku_selector": "img.src",
        "product_name_selector": "div.vtex-product-summary-2-x-nameContainer",
        "regular_price_selector": "span.wongio-store-theme-7-x-span-ref-value",
        "discount_price_selector": "span.vtex-product-price-1-x-sellingPrice",
        "image_selector": "img.src",
        "do_scroll": True,
        "browser": BaseScrapper.USE_CHROME,
        "show_browser": True,
        "verbose": True,
    }