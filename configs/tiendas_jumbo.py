from scrappers.base import BaseScrapper
from structures.products import JumboProduct

# TODO Se debe configurar paginador (funciona recorriendo la lista de elementos del paginador tiendasjumboqaio-jumbo-fetch-more-paginator-0-x-buttonPerPage)
config = {
        "pais": "Colombia",
        "fuente": "Tiendas Jumbo",
        "scrapper_class": BaseScrapper,
        "product_class": JumboProduct,
        "url": "https://www.tiendasjumbo.co/bandeja?_q=bandeja&map=ft",
        "search_placeholder": "bandeja",
        "product_selector": "div.vtex-search-result-3-x-galleryItem",
        "stop_behavior": BaseScrapper.STOP_IF_SELECTOR_IS_DISABLED,
        "page_type": BaseScrapper.SINGLE_PAGE,
        "pagination_selector": "a.vtex-button",
        "sku_selector": ".vtex-checkbox__input",
        "brand_selector": ".vtex-product-summary-2-x-productBrandName",
        "product_name_selector": ".vtex-product-summary-2-x-productBrand",
        "regular_price_selector": "section:nth-child(1) > a:nth-child(1) > article:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(2) > div:nth-child(1)",
        "discount_price_selector": "section:nth-child(1) > a:nth-child(1) > article:nth-child(1) > div:nth-child(1) > div:nth-child(5) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)",
        "image_selector": "img.vtex-product-summary-2-x-imageNormal",
        "do_scroll": True,
        "browser": BaseScrapper.USE_CHROME,
}