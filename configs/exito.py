from scrappers.base import BaseScrapper
from structures.products import ExitoProduct

config = {
        "pais": "Colombia",
        "fuente": "Exito.com",
        "scrapper_class": BaseScrapper,
        "url": "https://www.exito.com/guaro?_q=guaro&map=ft&page=pagenum",
        "product_class": ExitoProduct,
        "search_placeholder": "guaro",
        "page_placeholder": "pagenum",
        "product_selector": "div.vtex-search-result-3-x-galleryItem",
        "product_count_selector": ".vtex-search-result-3-x-totalProducts--layout > span:nth-child(1)",
        "stop_behavior": BaseScrapper.STOP_IF_SELECTOR_NOT_PRESENT,
        "page_type": BaseScrapper.SSR_PAGE,
        "pagination_selector": ".min-h-small",
        "sku_selector": "div.exito-buy-list-0-x-buttonAddToList",
        "brand_selector": "span.vtex-product-summary-2-x-productBrandName",
        "product_name_selector": "span.vtex-store-components-3-x-productBrand",
        "regular_price_selector": "div.exito-vtex-components-4-x-list-price",
        "discount_price_selector": "div.exito-vtex-components-4-x-PricePDP",
        "image_selector": "img.vtex-product-summary-2-x-image",
        "do_scroll": True,
        "browser": BaseScrapper.USE_CHROME,
        "show_browser": True,
        "verbose": True,
    }