import os
import sys
import fontforge
import psMat  
from constants import VECTORS_PATH, OTF_PATH, SDF_PATH


def escalar_y_centrar_glifo(glifo, factor_escala=0.8, margen_superior=50, margen_inferior=50):
    print(f"Procesando glifo: {glifo.glyphname}")
    
    # Mover el glifo a (0, 0)
    glifo.transform(psMat.translate(-glifo.boundingBox()[0], -glifo.boundingBox()[1]))
    print(f"Glifo trasladado a (0, 0).")

    # Obtener las dimensiones actuales del contorno
    xmin, ymin, xmax, ymax = glifo.boundingBox()
    print(f"Bounding Box antes de escalar: xmin={xmin}, ymin={ymin}, xmax={xmax}, ymax={ymax}")

    # Calcular el tamaño actual del glifo
    ancho_actual = xmax - xmin
    alto_actual = ymax - ymin
    print(f"Tamaño actual: ancho={ancho_actual}, alto={alto_actual}")

    # Calcular el factor de escala para que ocupe la mayoría del espacio
    escala_x = (800 * factor_escala) / ancho_actual
    escala_y = (800 * factor_escala) / alto_actual
    escala = min(escala_x, escala_y)  # Mantener la proporción
    print(f"Escala calculada: escala_x={escala_x}, escala_y={escala_y}, escala_final={escala}")
    print(f"Tamaño tras escala: ancho={ancho_actual * escala}, alto={alto_actual * escala}")

    # Comprobar si el glifo es demasiado grande
    if ((alto_actual * escala) or (ancho_actual * escala)) > (800 - margen_superior - margen_inferior):
        print(f"Fatal Error: La letra '{glifo.glyphname}' es demasiado grande para el espacio disponible.")
        sys.exit(1)  # Finaliza el programa con un código de error

    # Aplicar transformación: escalar y mover el glifo
    print(f"Aplicando escalado: {escala}")
    glifo.transform(psMat.scale(escala))  # Escalar
    print(f"Glifo escalado.")

    # Obtener las dimensiones del contorno tras escalado 
    xmin, ymin, xmax, ymax = glifo.boundingBox()
    print(f"Bounding Box despues de escalar: xmin={xmin}, ymin={ymin}, xmax={xmax}, ymax={ymax}")

    # Calcular el nuevo tamaño escalado
    ancho_escalado = xmax - xmin
    alto_escalado = ymax - ymin

    # Cálculo de offset para centrar en el eje X
    offset_x = (1000 - ancho_escalado) / 2 - xmin
    print(f"offset_x calculado: {offset_x} (xmin={xmin}, ancho_escalado={ancho_escalado})")

    # Cálculo de offset para centrar en el eje Y
    offset_y = (800 - alto_escalado) / 2 - ymin
    print(f"offset_y calculado: {offset_y} (ymin={ymin}, alto_escalado={alto_escalado})")

    # Aplicar la traslación para centrar el glifo
    print(f"Aplicando traslación: (offset_x={offset_x}, offset_y={offset_y})")
    glifo.transform(psMat.translate(offset_x, offset_y))
    print(f"Glifo trasladado.")

    # Ajustar el espaciado
    glifo.left_side_bearing = 50  # Ajustar el espaciado izquierdo
    glifo.right_side_bearing = 50  # Ajustar el espaciado derecho
    #print(f"Espaciado ajustado: left={glifo.left_side_bearing}, right={glifo.right_side_bearing}")

def cargar_svgs_y_generar_fuente(carpeta_svg, fontname):
    print(f"Creando fuente con nombre {fontname} desde {carpeta_svg}")
    
    # Crear una nueva fuente
    fuente = fontforge.font()

    # Ajustar el tamaño del em square y la altura de la fuente
    fuente.em = 1000
    fuente.ascent = 800  # Altura ascendente
    fuente.descent = 200  # Altura descendente
    print(f"Fuente configurada: em={fuente.em}, ascent={fuente.ascent}, descent={fuente.descent}")

    # Recorrer los archivos SVG en la carpeta
    for archivo_svg in os.listdir(carpeta_svg):
        print(f"Encontrado archivo: {archivo_svg}")
        
        if archivo_svg.endswith('.svg'):
            # Obtener el nombre del archivo sin la extensión (que es la letra o símbolo)
            nombre_archivo = os.path.splitext(archivo_svg)[0]
            print(f"Nombre del archivo (letra): {nombre_archivo}")

            # Convertir el nombre a su valor Unicode
            unicode_valor = ord(nombre_archivo[0])
            print(f"Valor Unicode para '{nombre_archivo}': {unicode_valor}")

            # Crear un nuevo glifo para este carácter
            glifo = fuente.createChar(unicode_valor)

            # Importar el contorno desde el archivo SVG
            ruta_svg = os.path.join(carpeta_svg, archivo_svg)
            print(f"Importando SVG desde: {ruta_svg}")
            glifo.importOutlines(ruta_svg, scale=True)

            # Escalar y centrar el glifo dentro del cuadro
            try:
                escalar_y_centrar_glifo(glifo, factor_escala=0.8, margen_superior=50, margen_inferior=50)
            except ValueError as e:
                print(e)

    # Crear bitmap strikes en diferentes tamaños (por ejemplo, 12, 16, 24 píxeles)
    # Los valores son en puntos, puedes agregar los tamaños que necesites
    tamaños_bitmap = ((32,),(48,),(64,),(96,),(128,),(256,))

    print(f'bitmapSizes actual: {fuente.bitmapSizes}')
    fuente.bitmapSizes = tamaños_bitmap

    # Generar los glifos en formato bitmap
    fuente.regenBitmaps()

    print(f'bitmapSizes tras regen: {fuente.bitmapSizes}')

    # Exportar la fuente en formato TTF
    fuente.fullname = fontname
    fuente.familyname = fontname
    fuente.fontname = fontname
    fuente.generate(OTF_PATH)
    fuente.save(SDF_PATH)
    print(f"Fuente generada correctamente: {fontname}")

# Ruta a la carpeta donde están almacenados los archivos SVG
carpeta_svg = VECTORS_PATH
# Nombre del archivo TTF que se va a generar
fontname = 'fuenteSalida'

# Llamar a la función para cargar los SVG y generar la fuente
cargar_svgs_y_generar_fuente(carpeta_svg, fontname)
