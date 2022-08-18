import os, csv, re, xlsxwriter, time
from PIL import Image
from urllib.error import HTTPError
from unicodedata import category
from urllib.request import urlopen, Request
from io import BytesIO
root_dir = "C:\\Users\\restreda\\Desktop\\DRN\WST\\"

#archivos
#input_file_path = os.path.join(root_dir, "resultado_cant.csv")
#output_file_path = os.path.join(root_dir, "resultado_cant.csv")
#file_exists = os.path.exists(output_file_path)
#mode = "w+" if not file_exists else "a"

fields = [
            "fecha",
            "sku",
            "pais",
            "fuente",
            "brand",
            "product_name",
            "precio_normal",
            "precio_descuento",
            "imagen",
            "cantidad",
            "unidad",
            "observacion",
            "categoria"
        ]

#with open(input_file_path, "r") as input_file:
  
##Inservar foto de URL##
# Crear el Libro
libro = xlsxwriter.Workbook(os.path.join(root_dir,"resultado_img.xlsx"))
# Crear la Hoja
hoja = libro.add_worksheet()
# Leer el archivo csv

input_file_path = os.path.join(root_dir, "resultado_cant.csv")
image_options = {
    'x_offset':        -40,
    'y_offset':        0,
    'x_scale':         0.07,
    'y_scale':         0.07,
    'object_position': 2,    
    'url':             None,
    'description':     None,
    'decorative':      False,
    }
with open(input_file_path, "r", encoding="ISO-8859-1") as input_file:
  reader = csv.DictReader(input_file)
  fila = 1
  hoja.write_row(0,0,fields+["foto"])
  for linea in reader:
    #print(f"Procesando {linea['product_name']}")
    hoja.write_row(fila,0,linea.values())
    # Abrir Imagen
    try:
      request_flag = Request(linea["imagen"],headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'})
      request_data = urlopen(request_flag)
      time.sleep(0.5)
      image_file = Image.open(BytesIO(request_data.read())).convert("RGB")
      image_file.thumbnail({400,300})
      image_file.save("temp.png", "png")

      with open("temp.png", "rb") as image_file:
        image_data = BytesIO(image_file.read())
      
      # Agregar las filas y columnas
      
        image_options.update({
            "url": None,
            'description': linea["product_name"],
            'image_data': image_data
            })
        # Agregar las Imagenes
        hoja.insert_image(fila, len(linea.values())+1, linea["imagen"], image_options)
    except (HTTPError,ValueError) as error:
      pass
    fila += 1

# Cerrar el archivo de excel
libro.close()