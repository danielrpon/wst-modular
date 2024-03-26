import re


class Product:
    sku = None
    ean = None
    brand = None
    product_name = None
    regular_price = None
    discount_price = None
    image = None

    def __init__(self, *args, **kwargs):
        for attribute, value in kwargs.items():
            # Verificar si tiene un metodo personalizado
            setter_name = attribute.replace("_selector", "_setter")
            if hasattr(self, setter_name):
                setter = getattr(self, setter_name)
                setter(value)
                continue

            # Caso por defecto
            if value is not None:
                setattr(self, attribute.replace("_selector", ""), value.text)

    def image_setter(self, value=None):
        """Establece un valor para la Imagen a partir de la url presente en el src"""
        if value is not None:
            self.image = value.attrs["src"]


class ExitoProduct(Product):
    def sku_setter(self, value=None):
        """Extractor personalizado del valor que contiene la etiqueta html para sku."""
        if value is not None:
            self.sku = value.attrs["id"]
        else:
            self.sku = ""

    def discount_price_setter(self, value=None):
        """Extractor personalizado del valor que contiene la etiqueta html para precio con descuento."""
        if value is not None:
            self.discount_price = value.text.replace(".", "")[2:]
        else:
            if self.regular_price:
                self.discount_price = self.regular_price

    def regular_price_setter(self, value=None):
        """VAlidador para el caso de los precios."""
        if value is not None:
            self.regular_price = value.text.replace(".", "")[2:]

        if self.discount_price is None:
            self.discount_price = self.regular_price


class FarmatodoProduct(Product):
    def sku_setter(self, value=None):
        """Establece un valor para el SKU a partir del data-cuf"""
        if value is not None:
            self.sku = value.attrs["data-cuf"]

    def get_cleaned_price(self, value=None):
        """Funcion auxilar para convertir $15.600 en 15600"""
        if value is not None:
            return value.text.replace(".", "")[1:]
        return None

    def regular_price_setter(self, value=None):
        """Asigna el valor del precio regular"""
        self.regular_price = self.get_cleaned_price(value=value)
        if self.discount_price is None:
            self.discount_price = self.regular_price

    def discount_price_setter(self, value=None):
        """Asigna el valor del precio con descuento"""
        if value is not None:
            self.discount_price = self.get_cleaned_price(value=value)
        else:
            if self.regular_price:
                self.discount_price = self.regular_price


class JumboProduct(Product):
    def sku_setter(self, value=None):
        """Procesa la información de SKU a partir del Checkbox de comparar."""
        if value is not None:
            self.sku = value.attrs["id"].split("-")[0]

    def get_cleaned_price(self, value=None):
        """Funcion auxilar para convertir $15.600 en 15600"""
        if value is not None:
            return value.text.replace(".", "")[2:]
        return None

    def regular_price_setter(self, value=None):
        """Asigna el valor del precio regular"""
        self.regular_price = self.get_cleaned_price(value=value)
        if self.discount_price is None:
            self.discount_price = self.regular_price

    def discount_price_setter(self, value=None):
        """Asigna el valor del precio con descuento"""
        if value is not None:
            self.discount_price = self.get_cleaned_price(value=value)
        else:
            if self.regular_price:
                self.discount_price = self.regular_price


class D1Product(Product):
    def get_cleaned_price(self, value=None):
        """Funcion auxilar para convertir $15.600 en 15600"""
        if value is not None:
            return value.text.replace(".", "")[2:]
        return None

    def sku_setter(self, value=None):
        """Procesa la información de SKU desde la url de la imagen."""
        if value is not None:
            self.sku = value.attrs["src"].split("/")[-1].split(".")[0]

    def product_name_setter(self, value=None):
        """Procesa la información de Nombre desde el ALT de la imagen."""
        if value is not None:
            self.product_name = value.attrs["alt"]

    def regular_price_setter(self, value=None):
        """Asigna el valor del precio regular"""
        self.regular_price = self.get_cleaned_price(value=value)
        if self.discount_price is None:
            self.discount_price = self.regular_price

    def discount_price_setter(self, value=None):
        """Asigna el valor del precio con descuento"""
        if value is not None:
            self.discount_price = self.get_cleaned_price(value=value)

        if self.discount_price == "":
            if self.regular_price:
                self.discount_price = self.regular_price

class OlimpicaProduct(Product):

    def ean_setter(self, value=None):
        """Procesa la información de EAN desde la url de la imagen."""
        if value is not None:
            href = value.attrs["href"]
            matches = re.search(r"-(\d*)-(\d*)\/p", href)
            if matches is not None:
                self.ean = matches.group(1)

    def sku_setter(self, value=None):
        """Procesa la información de SKU desde la url de la imagen."""
        if value is not None:
            href = value.attrs["href"]
            matches = re.search(r"-(\d*)-(\d*)\/p", href)
            if matches is not None:
                self.sku = matches.group(2)

    def regular_price_setter(self, value=None):
        """Asigna el valor del precio regular"""
        if value is not None:
            self.regular_price = self.get_cleaned_price(value=value.text[6:])
        if self.discount_price is None:
            self.discount_price = self.regular_price

    def discount_price_setter(self, value=None):
        """Asigna el valor del precio con descuento"""
        if value is not None:
            self.discount_price = self.get_cleaned_price(value=value.text)

        if self.discount_price == "" or self.discount_price is None:
            if self.regular_price:
                self.discount_price = self.regular_price

    def get_cleaned_price(self, value=None):
        """Funcion auxilar para convertir $15.600 en 15600"""
        if value is not None:
            return str(value.replace(".", "")[2:]).strip()
        return None


class MercadolibreProduct(Product):
    def sku_setter(self, value=None):
        """Procesa la información de SKU desde la url del producto."""
        if value is not None:
            href = value.attrs["href"]
            matches = re.search(r"/MCO-*([0-9]*)", href)
            if matches is not None:
                self.sku = matches.group(1)


    def regular_price_setter(self, value=None):
        if value is not None:
            matches = re.search(r"\w: (\d*)", value.text)
            if matches is not None:
                self.regular_price = matches.group(1)

    def discount_price_setter(self, value=None):
        if value is not None:
            matches = re.search(r"(\d*) ", value.text)
            if matches is not None:
                self.discount_price = matches.group(1)
                if self.regular_price is None:
                    self.regular_price = self.discount_price

class InkafarmaProduct(Product):
    def product_name_setter(self, value=None):
        if value is not None:
            self.product_name = value.attrs["alt"]

    def sku_setter(self, value=None):
        if value is not None:
            matches = re.search(r"/((\d.+)|(\w+\d+))", value.attrs["href"])
            if matches is not None:
                self.sku = matches.group(1)

    def discount_price_setter(self, value=None):
        if value is not None:
            matches = re.search(r"(\d.+)", value.contents[-1].text)
            if matches is not None:
                self.discount_price = matches.group(1)
                if self.regular_price is None:
                    self.regular_price = self.discount_price

    def regular_price_setter(self, value=None):
        if value is not None:
            matches = re.search(r"(\d.+)", value.contents[-1].text)
            if matches is not None:
                self.regular_price = matches.group(1)
                if self.discount_price is None:
                    self.discount_price = self.regular_price


class ZaraProduct(Product):
    def get_cleaned_price(self, value=None):
        """Funcion auxilar para convertir $15.600 en 15600"""
        if value is not None:
            return value.text.replace(".", "")[2:]
        return None

    def sku_setter(self, value=None):
        """Procesa la información de SKU desde la url de la imagen."""
        if value is not None:
            self.sku = value.attrs['data-productid']

    def product_name_setter(self, value=None):
        """Procesa la información de Nombre desde el ALT de la imagen."""
        if value is not None:
            self.product_name = value.attrs["alt"]

    def regular_price_setter(self, value=None):
        """Asigna el valor del precio regular"""
        self.regular_price = self.get_cleaned_price(value=value)
        if self.discount_price is None:
            self.discount_price = self.regular_price

    def discount_price_setter(self, value=None):
        """Asigna el valor del precio con descuento"""
        if value is not None:
            self.discount_price = self.get_cleaned_price(value=value)

        if self.discount_price == "":
            if self.regular_price:
                self.discount_price = self.regular_price