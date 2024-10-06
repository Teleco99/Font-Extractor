from Models.ImageModel import ImageModel
from tkinter import filedialog
from Models.AgruparService import AgruparService
import threading

class ImageController:
    def __init__(self):
        self.model = ImageModel()
        self.agruparService = AgruparService()
        self.processed_image = None

    def load_and_process_image(self, file_path, update_progress_callback):
        print(f"Procesando imagen desde {file_path}")
        processed_images = self.model.process_image(file_path, update_progress_callback)
        
        if processed_images:
            self.processed_image = processed_images

            # Notificamos a la barra de carga que se ha procesado la imagen
            finished = True
            progress = 100
            update_progress_callback(progress, finished)
            print("Imagen procesada correctamente")
        else:
            print("No se procesó ninguna imagen")

    def get_processed_image(self):
        # Asumimos que la imagen procesada es la última en la lista de imágenes
        if self.processed_image:
            return self.processed_image[-1]
        return None
    
    def open_file(self, update_callback):
        self.file_path = filedialog.askopenfilename(
            title="Seleccionar archivo de imagen", 
            filetypes=[("Imagen", "*.png;*.jpg;*.jpeg;*.bmp"), ("Todos los archivos", "*.*")]
        )

        if self.file_path:
            print(f"Archivo seleccionado: {self.file_path}")

            # Iniciar el hilo para procesamiento
            threading.Thread(target=self.load_and_process_image, args=(self.file_path, update_callback), daemon=True).start()

    
