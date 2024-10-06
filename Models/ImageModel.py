import cv2
import pytesseract
import os
from constants import ALPHABET_PATH, PATTERNS_PATH, TESSERACT_PATH

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH  # Cambia según tu ruta de instalación

class ImageModel:
    def __init__(self):
        self.alphabet_path = ALPHABET_PATH
        self.patterns_path = PATTERNS_PATH

        # Lista de rectángulos con coordenadas y letras
        self.rectangles = []  

    def process_image(self, image_path, update_progress_callback):
        if not os.path.exists(self.alphabet_path):
            os.makedirs(self.alphabet_path)
        #if not os.path.exists(self.patterns_path):
            #os.makedirs(self.patterns_path)

        image = cv2.imread(image_path)
        if image is None:
            print(f"Error al cargar la imagen desde {image_path}")
            return []

        print(f"Imagen cargada correctamente desde {image_path}")

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        print(f"Imagen convertida a escala de grises")

        # Convertir la imagen de BGR a RGB para que se muestre correctamente en Tkinter
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Aplicar un umbral
        _, image_umbralizada = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        print(f"Umbralización aplicada")

        # Encontrar contornos
        contours, _ = cv2.findContours(image_umbralizada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Invertir la imagen umbralizada para obtener letras negras sobre fondo blanco
        image_umbralizada = cv2.bitwise_not(image_umbralizada)

        min_area = 15
        filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]

        processed_images = []

        # Número total de contornos
        total_contours = len(filtered_contours)  

        for i, cnt in enumerate(filtered_contours):
            x, y, w, h = cv2.boundingRect(cnt)
            letter_image = image_umbralizada[y:y+h, x:x+w]
            pattern_image = image[y:y+h, x:x+w]

            if i > 200:
                continue

            # Posibles valores de lang
            # español: spa, spa_old
            # Orientation Script Detector: osd
            # latin: lat
            # ingles: eng
            recognized_letter = pytesseract.image_to_string(letter_image, lang='spa_old', config='--oem 1 --psm 10 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz').strip()
            if not recognized_letter:
                print(f"No se reconoció un carácter en el contorno {i}")
                recognized_letter = f"letter_{i}"
            else:
                if len(recognized_letter) > 1:  # Limitar el resultado a un solo carácter
                    recognized_letter = recognized_letter[0]

            # Llamamos callback para actualizar barra de progreso
            print(f"Reconocido caracter {recognized_letter}: {i} de {total_contours} contornos")
            progress = (i + 1) / total_contours * 100
            update_progress_callback(progress)

            #letter_folder = os.path.join(self.alphabet_path, recognized_letter)
            #if not os.path.exists(letter_folder):
                #os.makedirs(letter_folder)

            pattern_folder = os.path.join(self.patterns_path, recognized_letter)
            #if not os.path.exists(pattern_folder):
                #os.makedirs(pattern_folder)

            letter_path = os.path.join(self.alphabet_path, f"{recognized_letter}_{i}.png")
            #pattern_path = os.path.join(pattern_folder, f"{recognized_letter}_{i}.png")
            cv2.imwrite(letter_path, letter_image)
            #cv2.imwrite(pattern_path, pattern_image)

            # Se añade a lista de rectangulos
            self.rectangles.append((x, y, w, h, recognized_letter))

            # Se pintan los rectangulos sobre la imagen
            cv2.rectangle(image_rgb, (x, y), (x + w, y + h), (0, 255, 0), 2)

        processed_images.append(image_rgb)

        return processed_images

