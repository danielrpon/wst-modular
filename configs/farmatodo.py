from scrappers.base import BaseScrapper
from structures.products import FarmatodoProduct

config = {
        "pais": "Colombia",
        "fuente": "Farmatodo",
        "scrapper_class": BaseScrapper,
        "product_class": FarmatodoProduct,
        "url": "https://www.farmatodo.com.co/buscar?product=filemon&departamento=Todos&filtros=",
        "search_placeholder": "filemon",
        "product_selector": "div.card-ftd.mb-3",
        "stop_behavior": BaseScrapper.STOP_IF_SELECTOR_IS_DISABLED,
        "page_type": BaseScrapper.SINGLE_PAGE,
        "pagination_selector": "#group-view-load-more",
        "sku_selector": "a.product-image-link",
        "brand_selector": None,
        "product_name_selector": "div.text-left",
        "regular_price_selector": "span.text-price",
        "discount_price_selector": "span.text-offer-price",
        "image_selector": "img.image",
        "do_scroll": True,
        "browser": BaseScrapper.USE_CHROME,
        "show_browser": True,
        "verbose": True,
    }