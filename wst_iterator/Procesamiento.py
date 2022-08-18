# ojo con las cantidades en L con 1.5 litros no los toma.

# Generar Archivo de Entrada
import os, csv, re, xlsxwriter, time
from urllib.error import HTTPError
from unicodedata import category
from urllib.request import urlopen, Request
from io import BytesIO
root_dir = "C:\\Users\\restreda\\Desktop\\DRN\WST\\"

#archivos
input_file_path = os.path.join(root_dir, "resultado.csv")
output_file_path = os.path.join(root_dir, "resultado_cant.csv")
file_exists = os.path.exists(output_file_path)
mode = "w+" if not file_exists else "a"

#Patrones
# TODO: Esta expresión aun no evalua cosas como 2x100gr
# TODO: Crear diccionarios en funcion de la descripción para asignar un segmento (shampoo, acondicionador, desodorantes, combinados)
# Todo: Nombrar las combinaciones (shampoo+acondicionador, desodorante+talco)
# TODO: En el caso de combinados sumar las cantidades de los productos si estan en la misma unidad (ml, gr)
# TODO: Alternativamente se puede tomar una densidad para las unidades diferentes
#pattern_extract = r"((\d)*(X)+)*([0-9]+[.,]?[0-9]*|[.,]?[0-9]+)\s*(([LlMmGgUu]+[TtLlRrn]+[.*]*)|(Mil)|([Gg])|(Gramo)|(Gramos)|(Metro)|([G.])|([Un])|([Und])|(Grs)|(Mts)|(M)|(Ml\.*)|(m)|([Uu]+n[i]*d)|(L)|(Litro)|(Unidad)|(unidades)|(Unds)|(UN)|(Mililitro)|(Mililitros)|(Ml)|(Gr))+([\s]|$)"
pattern_extract = r"((\d)*(X)+)*([0-9]+[.,]?[0-9]*|[.,]?[0-9]+)\s*(([LlMmGgUu]+[TtLlRrn]+[.*]*)|(Mil)|([Gg]+\.*)|(Gramo)|(Gramos)|(Metro)|(Un)|(U\.*)|(Und)|(Grs)|(Mts)|(M)|(m)|([Uu]+n[i]*d)|(L)|(Litro)|(Unidad)|([Uu]+nidades)|(Unds)|(UN)|(Mililitro)|(Mililitros)|(Ml\))|(Gr\)))+([\s]|$)"
pattern_content = r"(\d+)(\s*)((\w[.,]*)+)(\s*)(\w+)"
equivalencias = { 'ml': 'Ml',
                  'ml.': 'Ml',
                  'Ml.': 'Ml',
                  'gr.':'Gr',
                  'g':'Gr',
                  'G.':'Gr',
                  'G':'Gr',
                 'gr':'Gr',
                 'Grs':'Gr',
                 'grs':'Gr',
                 'gramo':'Gr',
                 'gramos':'Gr',
                 'g...': 'Gr',
                 'g.': 'Gr',
                 'mil': 'Ml',
                 'ml...': 'Ml',
                 'ml)': 'Ml',
                 'mlt': 'Ml',
                 'Gr)': 'Gr',
                 'gr)': 'Gr',
                 'mililitro': 'Ml',
                 'mililitros': 'Ml',
                 'un': 'Und',
                 'u...': 'Und',
                 'u.': 'Und',
                 'Unds': 'Und',
                 'und': 'Und',
                 'unid': 'Und',
                 'unidad': 'Und',
                 'unidades': 'Und',
                 'unds': 'Und',
                 'un...': 'Und',
                 'Un': 'Und',
                 'UN': 'Und',
                 'U': 'Und',
                 'u' : 'Und',
                 'metros': 'Mts',
                 'mts': 'Mts',
                 'm': 'Mts',
                 'l': 'L',
                  'lt': 'L',
                 'litro': 'L',
                 'Litro': 'L'
                }

marcas = {
          "color trend": ["color trend"],
          "anew": ["anew"],
          "mark": ["mark"],
          "avon true" : ["avon","power stay"],
          "nivea": ["nivea"],
          "pantene":["pantene"],
          "koleston":["koleston"],
          "igora":["igora"],
          "palette":["palette"],
          "Koleston":["Koleston"],
          "l'oreal":["TINT" and "Casting","TINT" and "EXCELLENCE"],
          "HAR":["HAR"],
          "Garnier":["Garnier"],
          "ponds":["ponds","Pond'S","Pondï¿½S"],
          "delia":["delia"],
          "elvive":["elvive"],
          "savital":["savital"],
          "nailen":["nailen"],
          "samy":["samy"],
          "vogue":["vogue"],
          "maybelline":["Maybelline"], 
          "max factor":["Max Factor"],
          "covergirl":["Covergirl"],
          "vitu":["vitu "],   
          "gillette": ["gillete","Gillette","gilette"],
          "yodora": ["yodora"],
          "mexana": ["mexana"],
          "old spice": ["old spice"],
          "deo pies": ["deo pies"],
          "balance": ["Balance"],
          "obao": ["obao"],
          "menticol": ["menticol"],
          "babaria": ["babaria"],
          "lubriderm": ["lubriderm"],
          "natural Feeling" : ["natural feeling"],
          "speed stick": ["speed stick","Speed  Stick","Speedstick"],
          "lady speed stick": ["Lady Speed  Stick","Lady Speed Stick","Lady Speed"],
          "axe": ["exite", "axe "],
          "xen": ["xen "],
          "lea": [" lea"],
          "rexona" : ["rexona", "Ap Bamboo"],          
          "arden": ["arden"],
          "dove": ["dove", "men care"],
          "savital": ["savital"],
          "far away" : ["far away", "faraway", "rebel"],
          "colgate": ["colgate"],
          "sensodyne": ["sensodyne"],
          "johnson&johnson": ["johnson"],
          "gum": ["gum"],
          "kolynos": ["kolynos"],
          "vitis": ["vitis"],
          "dentito": ["dentito"],
          "dento": ["dento"],
          "sensofluor": ["sensofluor"],
          "cristop": ["cristop"],
          "denture": ["denture"],
          "miniso": ["miniso"],
          "infly": ["infly"],
          "curapox": ["curapox"],
          "dentek": ["dentek"],
          "soral": ["soral"],
          "listerine": ["listerine"], 
          "perio aid": ["perio aid"],   
          "oral fresh": ["oral fresh"],
          "weir": ["weir"],
          "oralsept": ["oralsept"],
          "gingivit": ["gingivit"],                     
          "oral-b": ["oral-b","oral b","oralb"]
          }

categorias = {
          "hair care": ["shampoo", "champú", "acondicionador", "tinte", "peinar", "capilar", "tintura"],
          "body care": ["desodorante", "deo", "roll on", "rollon", "desod", "Desodor", "Desodo", "Corporal", "protector solar", "lubriderm","antitranspirante"],
          "color": ["labial", "brillo labial", "polvo", "base", "mascara", "delineador", "lapiz", "lápiz", "máscara", "pestañas", "rubor", "brillo para labios", "sombras", "esmalte","polvo compacto", "polvo-base", "base-polvo"],
          "face care": ["Facial", "limpiadora", "agua micelar", "antiarrugas", "serum", "skin ", "bloqueador facial", "antiedad", "antimanchas", "face", "ponds", "Pond'S"],
          "fragrance" : ["eua", "perfume"],
          "oral" : ["crema dental", "pasta dental", "hilo dental", "ceda dental",  "cepillo dental", "cepillo de dientes", "enjuague bucal"]
        }

segmentos = {
          "labios": ["labial", "delieador labios"],
          "rostro": ["polvo compacto", "compacto polvo","base-polvo", "polvo y base", "base y polvo", "Polvo Vogue"],
          "rubor" : ["rubor", "blush"],
          "shampoo": ["shampoo", "champú"],
          "acondicionador": ["acondicionador", "bálsamo", "balsamo"],
          "Crema Para Peinar": ["Crema Para Peinar"],
          "Desodorante": ["roll on", "rollon", "desodorante", "deo spray","antitranspirante"],
          "Crema Humectante" : ["Lubriderm", "Crema Piel"],
          }

formas = {
          "gel": [("gel", "desodorante"), ("crema","desodorante")],
          "spray": [("spray","desodorante"),("aerosol","desodorante")],
          "barra": [("barra", "desodorante"), ("barra","desodorante")],
          "roll on": [("roll on" , "desodorante"), ("roll" , "on" , "desodorante")],
          "labial": [("labial",), ("lipstick",), ("lipgloss",), ("lip ", "gloss")],
          "polvo compacto": [("polvo compacto",), ("polvo vogue compacto",)],
          "polvo-base": [("Base-polvo",), ("base-polvo",), ("polvo y base",) ,("base y polvo",)],
          "rubor": [("rubor",),("blush",)],
          "shampoo 170 Ml": [("shampoo","170")],
          }

referencias = {
          #Labiales
            #VOGUE
          "Labial Vogue Colorissimo Larga Duración 8hrs 2 Gr": ["17190","17201","17212","301568","1046505","1046502","1046506","1048439","1048434","1046507","1046503","1046508","1052837","208900083","208850215","208850207","208850194","208850186","208850178","208850135","208850135","1055410","1055411","1055609","1055608","1055608","1055607","1055607","1055606","1055606","17208","106161881","106161890","106111817","1048441","1048441","1052836","1052836","1052839","1052839"],
          "Labial Vogue Mate 4 Gr ": ["179074",	"179052",	"179058"],
          "Labial Vogue Sedoso 4 Gr": ["179078",	"179066"],
          "Labial Vogue Super Fantastic 4 Gr": ["1055599","1055602","1055600","963729"],
          "Labial Vogue Colorissimo Cremoso Mate 8hrs 4 Gr": ["203150201","203150210","203150199","203150181","203150172","203150164","203150148","203150121","203150113","203150105","203150092","203150156"],
            #AVON
          "Color Trend Mi Favorito Lapiz Labial Hidratante Semimate 1,5 Gr": ["1221399"],
          "Avon Labial Cremoso Legend FPS 15 3,6 Gr": ["1220005"],
          "Avon Lapiz Labial Matte Legend FPS 15 3,6 Gr": ["1203228"],
          "Color Trend Labial Efecto Metalico FPS 15 3.6 Gr": ["1198642"],
          "Color Trend Lapiz Labial Efecto Mate FPS 15 3.6 Gr": ["1194255",],
          "Avon Labial 8 En 1 FPS 15 3,6 Gr": ["1222177"],
          "Avon Labial Luminous Matte FPS 15 3,6 Gr": ["1196919"],
          "Avon Lapiz Labial Ultramate FPS 15 3,6 Gr": ["1222636"],
          "Avon Ultra Gloss Brillo Labial 7 Ml": ["1220717"],
          "Brillo Labial Avon Fantasy Cat 7 Gr": ["1228470"],
          "Color Trend Barrita 2 En 1 Labial y Rubor 4.5 Gr": ["1224589"],
          "Color Trend Barrita Labial Con Sabor 4,5 Gr": ["1195740"],
          "Color Trend Brillo Labial Fruity Gloss 10 Gr": ["1203474"],
          "Color Trend Labial Liquido Creamy Dlicious 4 Ml": ["1200110", "1221045", "1223074"],
          "Color Trend Lapiz Labial Efecto Mate FPS 15 3.6 Gr": ["1223076","1204396","1194255"],
          "Color Trend Lapiz Labial Hidratante FPS 15 3.6 Gr": ["1204395","1194264"],
          "Color Trend Volumatte Labial Efecto Mate FPS 15 3.6 Gr": ["1220220"],
          "Labial de Larga Duracion FPS 15 - 1.5 Gr": ["1192025"],
          "Labial Liquido Metallic Matte 4 Ml": ["1202160"],
          "Labial Liquido Ultra Lip Paint FPS 15 7 Ml": ["1222996"],
          "Lapiz Labial Extra Volumen FPS 15 - 3.6 Gr": ["1056034"],
          "Mark Labial Delineador 2 en 1 Tattoo 1.6 Ml": ["1202009"],
          "Mark Labial Liquido Mate FPS 15 7 Ml": ["1194237"],
          "Mark Lapiz Labial Epic FPS 15 3,6 Gr": ["1194534"],
          "Mark Lapiz Labial Prism FPS 15 3.6 Gr": ["1200093"],
          "Mark Show Glow Brillo Labial Efecto Holocromatico 4 Ml": ["1220689"],
          "Power Stay Labial Liquido 7 Ml": ["1203490"],

          #Polvo Compacto
            #VOGUE
          "Polvo Vogue Compacto Resist 14 Gr": ["71127","1061314","1061316","1061313","1061315"],
          "Polvo Vogue Compacto Mate Natural 14 Gr": ["912481","208900260","208900260","208900251","208900251","208900243","208900243","208900235","208900235","208900227","208900227","208900219","208900201","208900198","208900180","1063139"],
          
            #AVON
          "Anew Polvo Compacto Transformador FPS 15 10 Gr": ["1138497"],
          "Avon Polvo Compacto Matificante 11 Gr": ["1193475"],
          "Avon Precious Earth Polvo Compacto Efecto Bronceador 10.5 Gr": ["1223340"],
          "Color Trend Polvo Compacto Facial 7 Gr": ["1194260"],
          "Color Trend Polvo Compacto Facial Efecto Mate FPS 10 7 Gr": ["1194263"],
          "Base y Polvo Doble Funcion FPS 15 9 Gr": ["1193476"],
          
          
          #Polvo y Base
          "Base-polvo Vogue Efecto Total 14 Gr":["1055403"],
          }

# Lectura
with open(input_file_path, "r") as input_file:
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
            "categoria",
            "segmento",
            "forma",
            "referencia"
        ]

  with open(output_file_path, mode, newline="", encoding="ISO-8859-1") as output_file:
    writer = csv.DictWriter(output_file, fieldnames=fields)
    #Encabezados de Salida
    writer.writeheader()
    
    reader = csv.DictReader(input_file)

    for linea in reader:

      linea['categoria'] = ""
      linea['segmento'] = ""
      linea['forma'] = ""
      linea['referencia'] = ""

      cadena_contenido = re.search(pattern_extract, linea['product_name'])
      coincidencias = re.findall(pattern_extract, linea['product_name'])
      observacion = ""
      unidad = 'Und'
      cantidad = 1
      #Se requiere una excepción para los casos de .
      #if unidad = ".":

      #Agregar observacion de multiples coincidencias
      if len(coincidencias) and not coincidencias[0][1]:
        cantidad = 0
        for index, coincidencia in enumerate(coincidencias):
          unidad_de_coincidencia = equivalencias.get(coincidencia[4].lower(), coincidencia[4].lower())
          if index == 0:
            unidad = unidad_de_coincidencia
            
          if unidad_de_coincidencia == unidad:
            cantidad += float(coincidencia[3].replace(',','.'))
            #print(cantidad)
          else:
            observacion += f"+ {coincidencia[3]} {equivalencias.get(coincidencia[4].lower(), coincidencia[4].lower())}"
      elif len(coincidencias) and coincidencias[0][1]:
        cantidad = 0
        unidad_de_coincidencia = equivalencias.get(coincidencias[0][4].lower(), coincidencias[0][4].lower())
        if unidad_de_coincidencia == "Und":
          try:
            cantidad = float(coincidencias[0][3].replace(',','.')) * float(coincidencias[0][1].replace(',','.'))
            #print(cantidad)
            unidad = equivalencias.get(coincidencias[0][4].lower(), coincidencias[0][4].lower())
          except (TypeError,ValueError) as error:
            print(error,"1")
            pass  
      elif len(coincidencias) == 3:
        cantidad = 0
        unidad_de_coincidencia = equivalencias.get(coincidencias[0][4].lower(), coincidencias[0][4].lower())
        if unidad_de_coincidencia == "Und":
          cantidad = int(coincidencias[0][3]) * int(coincidencias[1][3])
          #print(cantidad)
          unidad = equivalencias.get(coincidencias[1][4].lower(), coincidencias[1][4].lower())
          observacion += f"+ {coincidencias[2][3]} {equivalencias.get(coincidencias[2][4].lower(), coincidencias[2][4].lower())}"


      if cadena_contenido is not None and not cantidad:
        valores = re.search(pattern_content, cadena_contenido.group())
        if valores is not None:
          cantidad = valores.group(0)
          #print(cantidad)
          unidad = equivalencias.get(valores.group(5).lower(), "Und")
        #Verificaba sí tiene un multiplicador en la posición 1
        if cadena_contenido.group(1) is not None:
          #print(f"{linea['product_name']},grupo 2:{cadena_contenido.group(2)},grupo 4:{cadena_contenido.group(4)}")
          try:
            cantidad = float(cadena_contenido.group(2)) * float(cadena_contenido.group(4).replace(',','.'))
            #print(cantidad)
          except (TypeError,ValueError) as error:
            print(error)
            pass
          unidad = equivalencias.get(cadena_contenido.group(5).lower(), "Und")
          
      # Bloque Procesamiento de Marcas (Brand)
      if linea["brand"] == "":
          for marca, patrones in marcas.items():
              if any(
                  [
                      patron
                      for patron in patrones
                      if patron.lower() in linea['product_name'].lower()
                  ]
              ):
                  linea["brand"] += f"{marca.title()}, "
          linea['brand'] = linea['brand'].strip(", ").title()
      
      if linea["categoria"] == "":
          for categoria_, patrones in categorias.items():
              if any(
                  [
                      patron
                      for patron in patrones
                      if patron.lower() in linea["product_name"].lower()
                  ]
              ):
                  linea['categoria'] += f"{categoria_.title()}, "
          linea['categoria'] = linea['categoria'].strip(", ")
          pass  

      if linea["segmento"] == "":
          for segmento, patrones in segmentos.items():
              if any(
                  [
                      patron
                      for patron in patrones
                      if patron.lower() in linea["product_name"].lower()
                  ]
              ):
                  linea['segmento'] += f"{segmento.title()}, "
          linea['segmento'] = linea['segmento'].strip(", ")
          pass  
      
      
      if linea["forma"] == "":
          encontrado = False
          for forma, patrones in formas.items():
              if encontrado :
                break            
              for patron_tupla in patrones:
                if encontrado :
                  break                 

                if all(
                    [
                        True if patron.lower() in linea["product_name"].lower() else False                        
                        for patron in patron_tupla
                    ]
                ):
                    linea['forma'] += f"{forma.title()}, "
                    encontrado = True

                  
          linea['forma'] = linea['forma'].strip(", ")
            

      if linea["referencia"] == "":
          for referencia, patrones in referencias.items():
              if any(
                  [
                      patron
                      for patron in patrones
                      if patron.lower() in linea["sku"]
                  ]
              ):
                  linea['referencia'] += f"{referencia.title()}, "
          linea['referencia'] = linea['referencia'].strip(", ")
          pass

      if cantidad ==1 and unidad == 'Und' or cantidad ==1 and unidad == '.':
          cadena_contenido = re.search(pattern_extract, linea['referencia'])
          coincidencias = re.findall(pattern_extract, linea['referencia'])
          #cantidad = 0
          for index, coincidencia in enumerate(coincidencias):
            unidad_de_coincidencia = equivalencias.get(coincidencia[4].lower(), coincidencia[4].lower())
            if index == 0:
              unidad = unidad_de_coincidencia
            if unidad_de_coincidencia == unidad:
              cantidad += float(coincidencia[3].replace(',','.'))
              #print(cantidad)
            else:
              observacion += f"+ {coincidencia[3]} {equivalencias.get(coincidencia[4].lower(), coincidencia[4].lower())}"
      
      linea['fecha']= linea['fecha'][0:10]
      linea['pais'] = linea['pais'].title()
      linea['fuente'] = linea['fuente'].title()
      linea['brand'] = linea['brand'].title()
      linea['product_name'] =  linea['product_name'].replace(',','.').replace('"','').replace('$','').title()
      linea['unidad'] = unidad
      linea['cantidad'] = cantidad
      linea['observacion'] = observacion.strip(" ")
      
      # print( linea['unidad'], linea['cantidad'])
      writer.writerow(linea)

###Inservar foto de URL##
## Crear el Libro
#libro = xlsxwriter.Workbook(os.path.join(root_dir,"resultado_img.xlsx"))
## Crear la Hoja
#hoja = libro.add_worksheet()
## Leer el archivo csv

#input_file_path = os.path.join(root_dir, "resultado_cant.csv")
#image_options = {
#    'x_scale':         0.07,
#    'y_scale':         0.07,
#    'object_position': 2,    
#    'url':             None,
#    'description':     None,
#    'decorative':      False,
#    }
#with open(input_file_path, "r", encoding="ISO-8859-1") as input_file:
#  reader = csv.DictReader(input_file)
#  fila = 1
#  hoja.write_row(0,0,fields+["foto"])
#  for linea in reader:
#    print(f"Procesando {linea['product_name']}")
#    hoja.write_row(fila,0,linea.values())
#    # Abrir Imagen
#    try:
#      request_flag = Request(linea["imagen"],headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'})
#      request_data = urlopen(request_flag)
#      time.sleep(0.5)
#      image_data = BytesIO(request_data.read())
#      # Agregar las filas y columnas
      
#      image_options.update({
#          "url": None,
#          'description': linea["product_name"],
#          'image_data': image_data
#          })
#      # Agregar las Imagenes
#      hoja.insert_image(fila, len(linea.values())+1, linea["imagen"], image_options)
#    except (HTTPError,ValueError) as error:
#      pass
#    fila += 1

# Cerrar el archivo de excel
#libro.close()