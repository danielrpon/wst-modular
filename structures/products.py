class Product:
    sku = None
    brand = None
    product_name = None
    regular_price = None
    discount_price = None
    image = None

    def __init__(self, *args, **kwargs):
        for attribute, value in kwargs.items():
            # Verificar si tiene un metodo personalizado
            if hasattr(self, f"{attribute}_setter"):
                setter = getattr(self, f"{attribute}_setter")
                setter(value)
                continue

            # Caso por defecto
            if value is not None:
                setattr(self, attribute.replace("_selector", ""), value.text)


class ExitoProduct(Product):
    def sku_setter(self, value=None):
        """Extractor personalizado del valor que contiene la etiqueta html para sku."""
        self.sku = value["attrs"]["name"]

    def discount_price_setter(self, value=None):
        """Extractor personalizado del valor que contiene la etiqueta html para precio con descuento."""
        if value is not None:
            self.discount_price = value.text
        else:
            if self.regular_price:
                self.discount_price = self.regular_price

    def regular_price_setter(self, value=None):
        """VAlidador para el caso de los precios."""
        if value is not None:
            self.regular_price = value.text

        if self.discount_price is None:
            self.discount_price = self.regular_price

    def image_setter(self, value=None):
        if value is not None:
            self.image = value["attrs"]["src"]
