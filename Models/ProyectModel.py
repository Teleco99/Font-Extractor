import os
import cv2
import subprocess
import potrace
import shutil
from constants import VECTORS_PATH, ALPHABET_PATH, ALPHABET_GROUPED_PATH, SCRIPT_CREATE_PATH

class ProyectModel:
    def __init__(self):
        # Ruta de la carpeta con las imágenes y la carpeta de salida
        self.output_folder = VECTORS_PATH
        self.letrasMinusculasSeleccionadas = []
        self.letrasMayusculasSeleccionadas = []

    def es_mayuscula(self, key):
        """Devuelve True si la clave es mayúscula, False si es minúscula."""
        return len(key) == 2  # Considerando que las mayúsculas tienen longitud 2

    def insert_value_in_list(self, key, index, new_value):
        """Inserta un nuevo valor en la lista dada su clave y posicion, moviendo los elementos a la derecha."""

        if self.es_mayuscula(key):
            letrasSeleccionadas = self.letrasMayusculasSeleccionadas
        else:
            letrasSeleccionadas = self.letrasMinusculasSeleccionadas

        # Verificar si la clave existe en el diccionario
        if key in letrasSeleccionadas:
            # Obtener la lista correspondiente a la clave
            lista = letrasSeleccionadas[key]

            # Asegurarse de que el índice esté dentro del rango de la lista
            if 0 <= index <= len(lista):
                # Usar insert() para agregar el nuevo valor en la posición indicada
                lista.insert(index, new_value)
            else:
                print(f"Indice fuera de rango: {key}")
        else:
                print(f"La clave '{key}' no existe en el diccionario.")

    def get_image_paths_by_folder_name(self, base_folder):
        # Inicializar diccionarios con las claves de todo el abecedario
        letras_minusculas = {chr(i): [] for i in range(ord('a'), ord('z') + 1)}
        letras_mayusculas = {f"{chr(i)}{chr(i).lower()}": [] for i in range(ord('A'), ord('Z') + 1)}

        # Recorre cada subcarpeta en la carpeta principal
        for folder_name in os.listdir(base_folder):
            folder_path = os.path.join(base_folder, folder_name)

            # Verifica si es una carpeta
            if os.path.isdir(folder_path):
                image_paths = []

                # Recorre los archivos dentro de la subcarpeta y guarda las rutas de las imágenes
                for filename in os.listdir(folder_path):
                    if filename.endswith(('.png', '.jpg', '.jpeg')):
                        image_path = os.path.join(folder_path, filename)
                        image_paths.append(image_path)

                # Clasifica las carpetas según el nombre de la carpeta
                if len(folder_name) == 1 and folder_name in letras_minusculas:
                    # Si es una carpeta con un solo carácter en minúscula
                    letras_minusculas[folder_name] = image_paths
                elif len(folder_name) == 2 and folder_name in letras_mayusculas:
                    # Si es una carpeta con dos caracteres (mayúscula + minúscula)
                    letras_mayusculas[folder_name] = image_paths

        self.letrasMinusculasSeleccionadas = letras_minusculas
        self.letrasMayusculasSeleccionadas = letras_mayusculas

        return letras_minusculas, letras_mayusculas
    
    def generar_vectores(self, mayuscula=False):
        # Asegurarse de que la carpeta de salida existe
        os.makedirs(self.output_folder, exist_ok=True)

        dicLetras = self.letrasMinusculasSeleccionadas
        if mayuscula:
            dicLetras = self.letrasMayusculasSeleccionadas

        for char, characterFiles in dicLetras.items():
            if characterFiles:
                # Usar la primera imagen de cada lista
                if characterFiles[0].lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                    print(f'Generando SVG de fichero {characterFiles[0]}')
                        
                    # Cargar la imagen y convertirla a blanco y negro
                    image = cv2.imread(characterFiles[0], cv2.IMREAD_GRAYSCALE)
                    _, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)

                    # Convertir a un formato que potrace pueda utilizar
                    bitmap = potrace.Bitmap(binary_image)
                    path = bitmap.trace()

                    # Crear un archivo SVG con el nombre de la carpeta
                    output_filename = f'{char}.svg'
                    output_path = os.path.join(self.output_folder, output_filename)
                        
                    with open(output_path, 'w') as svg_file:
                        svg_file.write('<svg xmlns="http://www.w3.org/2000/svg">\n')
                            
                        for curve in path:
                            svg_file.write('<path d="M ')
                            start_point = curve.start_point
                            svg_file.write(f'{start_point.x} {start_point.y} ')
                                
                            for segment in curve.segments:
                                if segment.is_corner:
                                    # Segmento de esquina
                                    x, y = segment.c.x, segment.c.y
                                    end_x, end_y = segment.end_point.x, segment.end_point.y
                                    svg_file.write(f'L {x} {y} L {end_x} {end_y} ')
                                else:
                                    # Segmento de curva Bezier
                                    x1, y1 = segment.c1.x, segment.c1.y
                                    x2, y2 = segment.c2.x, segment.c2.y
                                    end_x, end_y = segment.end_point.x, segment.end_point.y
                                    svg_file.write(f'C {x1} {y1}, {x2} {y2}, {end_x} {end_y} ')
                                
                            svg_file.write('"/>\n')
                        
                        svg_file.write('</svg>\n')

                        print(f'Se ha generado el SVG para: {char}')

    def generar_fuente(self):  
        # Ejecutar createFont desde ffpython  
        process = subprocess.Popen(
            ['ffpython', SCRIPT_CREATE_PATH],  # Comando o script a ejecutar
            stdout=subprocess.PIPE,  # Captura la salida estándar
            stderr=subprocess.PIPE,  # Captura los errores
            universal_newlines=True  # Asegura que las salidas se traten como cadenas de texto
        )

        # Leer la salida línea por línea
        for stdout_line in iter(process.stdout.readline, ""):
            print(f"Salida: {stdout_line.strip()}")  # Mostrar la salida en tiempo real

        # Leer la salida de errores (stderr)
        for stderr_line in iter(process.stderr.readline, ""):
            print(f"Error: {stderr_line.strip()}")  # Mostrar los errores en tiempo real

        process.stdout.close()
        process.stderr.close()

        # Esperar a que el proceso termine
        process.wait()

    def copy_image_to_folder(self, imagen_path, destino_folder):
        # Obtener el nombre de archivo de la imagen
        nombre_imagen = os.path.basename(imagen_path)
        
        # Construir la ruta destino (se asume que el directorio ya existe)
        destino_path = os.path.join(destino_folder, nombre_imagen)

        # Copiar la imagen a la carpeta destino
        shutil.copy(imagen_path, destino_path)
        print(f"Imagen copiada a: {destino_path}")

    def borrar_carpetas(self):
        carpetas_a_borrar = [ALPHABET_PATH, ALPHABET_GROUPED_PATH, VECTORS_PATH]
    
        for carpeta in carpetas_a_borrar:
            try:
                if os.path.exists(carpeta):
                    shutil.rmtree(carpeta)  # Elimina la carpeta y su contenido
                    print(f'Carpeta {carpeta} eliminada.')
                else:
                    print(f'La carpeta {carpeta} no existe.')
            except Exception as e:
                print(f'Error al eliminar la carpeta {carpeta}: {e}')


        
                        