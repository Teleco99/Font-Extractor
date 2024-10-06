import os
import shutil
from constants import ALPHABET_GROUPED_PATH

class AgruparService:

    def format_folder_name(self, character):
        """Formatea el nombre de la carpeta. Mayúsculas van como Aa, minúsculas tal cual."""
        if character.isupper():
            # Si es mayúscula, devuelve el formato Aa
            return f"{character}{character.lower()}"
        else:
            # Si es minúscula, devuelve el carácter tal cual
            return character

    def create_folders(self, base_folder):
        """Crea todas las carpetas (Aa, Bb, ..., a, b, c, ...) para agrupar las imágenes."""
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        for char in alphabet:
            # Crear carpetas Aa, Bb, ..., Zz
            upper_folder_name = self.format_folder_name(char.upper())
            upper_folder_path = os.path.join(base_folder, upper_folder_name)
            if not os.path.exists(upper_folder_path):
                os.makedirs(upper_folder_path)

            # Crear carpetas a, b, c, ..., z
            lower_folder_path = os.path.join(base_folder, char)
            if not os.path.exists(lower_folder_path):
                os.makedirs(lower_folder_path)

    def move_files_to_existing_folder(self, image_urls, dest_folder):
        """Mueve los archivos de imagen a la carpeta de destino, renombrando si es necesario."""
        for image_url in image_urls:
            filename = os.path.basename(image_url)
            dest_file_path = os.path.join(dest_folder, filename)
            
            # Copiar la imagen a la carpeta de destino
            shutil.copy(image_url, dest_file_path)

    def group_images_by_character(self, image_folder, base_folder):
        """Agrupa las imágenes según el primer carácter del nombre del archivo."""
        images = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
        print(f"Imágenes encontradas: {images}")

        for img_name in images:
            # Obtener el primer carácter del nombre del archivo
            character = img_name[0]

            # Definir el nombre de la carpeta donde se moverá la imagen
            if character.isalpha():
                folder_name = self.format_folder_name(character)
                dest_folder = os.path.join(base_folder, folder_name)

                # Mover la imagen a la carpeta correspondiente
                self.move_files_to_existing_folder([os.path.join(image_folder, img_name)], dest_folder)
                print(f"Imagen {img_name} movida a la carpeta {folder_name}.")
            else:
                print(f"El archivo {img_name} no tiene un carácter válido para agrupar.")

    def agrupar(self, image_folder):
        """Agrupa las imágenes directamente según el prefijo de su nombre."""
        # Verificar si se seleccionó una carpeta
        if image_folder:
            print(f"Ruta de la carpeta seleccionada: {image_folder}")

            # Crear todas las carpetas necesarias (Aa, Bb, ..., a, b, c, ...)
            base_folder = ALPHABET_GROUPED_PATH
            self.create_folders(base_folder)

            # Agrupar las imágenes directamente por el prefijo de su nombre
            self.group_images_by_character(image_folder, base_folder)

            print("Imágenes agrupadas.")
        else:
            print("No se seleccionó ninguna carpeta.")
