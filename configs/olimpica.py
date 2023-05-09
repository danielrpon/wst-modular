from scrappers.base import D1Scrapper, BaseScrapper, OlimpicaScrapper
from structures.products import D1Product, OlimpicaProduct

config = {
        "pais": "Colombia",
        "scrapper_class": OlimpicaScrapper,
        "product_class": OlimpicaProduct,
        "fuente": "Olimpica",
        "url": "https://www.olimpica.com/placeholder?_q=placeholder&map=ft&page=pagenum",
        "search_placeholder": "placeholder",
        "page_placeholder": "pagenum",
        "product_count_selector": "div.vtex-search-result-3-x-totalProducts--layout",
        "product_selector": "div.vtex-search-result-3-x-galleryItem",
        "producs_per_page": 12,
        "stop_behavior": BaseScrapper.STOP_IF_NO_PRODUCTS,
        "page_type": BaseScrapper.SSR_PAGE,
        "ean_selector": "a.vtex-product-summary-2-x-clearLink--product-summary",
        "sku_selector": "a.vtex-product-summary-2-x-clearLink--product-summary",
        "product_name_selector": "span.vtex-product-summary-2-x-productBrand",
        "discount_price_selector": "div.vtex-product-price-1-x-sellingPrice--hasListPrice--dynamicF",
        "regular_price_selector": "div.olimpica-dinamic-flags-0-x-strikePrice",
        "image_selector": "img.vtex-product-summary-2-x-image",
        "do_scroll": True,
        "browser": BaseScrapper.USE_CHROME,
        "show_browser": True,
        "verbose": True,
}