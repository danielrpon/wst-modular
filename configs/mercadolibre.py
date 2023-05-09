from scrappers.base import MercadolibreScrapper
from structures.products import MercadolibreProduct

config = {
        "pais": "Colombia",
        "fuente": "Mercadolibre Colombia",
        "scrapper_class": MercadolibreScrapper,
        "product_class": MercadolibreProduct,
        "url": "https://listado.mercadolibre.com.co/placeholder",
        "search_placeholder": "placeholder",
        "product_selector": "li.ui-search-layout__item",
        "stop_behavior": MercadolibreScrapper.STOP_IF_SELECTOR_NOT_PRESENT,
        "page_type": MercadolibreScrapper.SINGLE_PAGE,
        "pagination_selector": "a.andes-pagination__link.shops__pagination-link.ui-search-link[title='Siguiente']",
        "sku_selector": "a.ui-search-link",
        "brand_selector": "span.ui-search-item__brand-discoverability",
        "product_name_selector": "h2.ui-search-item__title",
        "regular_price_selector": "s.ui-search-price__original-value",
        "discount_price_selector": "div.ui-search-price__second-line.shops__price-second-line",
        "image_selector": "img.ui-search-result-image__element.shops__image-element",
        "do_scroll": True,
        "browser": MercadolibreScrapper.USE_CHROME,
}