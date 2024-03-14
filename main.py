import csv
import datetime
import os

from configs import all_configurations

configuraciones = all_configurations
#
# CSV
output_file_path = os.path.join("./", "output.csv")
file_exists = os.path.exists(output_file_path)
mode = "w+" if not file_exists else "a"
with open(output_file_path, mode, newline="", encoding="ISO-8859-1") as output_file:
    # Encabezados
    fields = [
        "fecha",
        "sku",
        "ean",
        "pais",
        "fuente",
        "brand",
        "product_name",
        "precio_normal",
        "precio_descuento",
        "imagen",
    ]
    writer = csv.DictWriter(output_file, fieldnames=fields)
    if not file_exists:
        writer.writeheader()

    for fuente in configuraciones:
        # Instanciar un scrapper (por fuente)
        scrapper_class = fuente["scrapper_class"]
        scrapper = scrapper_class(
            **fuente
        )

        for index, product in enumerate(scrapper.get_products("Pantene")):
            writer.writerow(
                {
                    "fecha": datetime.datetime.now(),
                    "sku": product.sku,
                    "ean": product.ean,
                    "pais": fuente["pais"].title(),
                    "fuente": fuente["fuente"].title(),
                    "brand": product.brand,
                    "product_name": product.product_name,
                    "precio_normal": product.regular_price,
                    "precio_descuento": product.discount_price,
                    "imagen": product.image
                }
            )