import tkinter as tk
import cv2
from tkinter import ttk, Menu
from PIL import Image, ImageTk
from constants import ALPHABET_PATH

class ImageView:
    def __init__(self, root, imageController, loaded_callback):
        self.root = root
        self.imageController = imageController
        self.image_loaded_callback = loaded_callback

        self.root.title("Manuscript")

        # Crear el menú
        self.root.menu = Menu(root)
        self.root.config(menu=self.root.menu)

        # Crear submenus
        self.submenu_archivo = Menu(self.root.menu, tearoff=0)
        self.root.menu.add_cascade(label="Archivo", menu=self.submenu_archivo)

        # Opción para abrir archivo
        self.submenu_archivo.add_command(label="Abrir archivo", command=lambda: self.imageController.open_file(self.update_progress_thread))

        # Crear un contenedor para contener la imagen original
        self.image_container = ttk.LabelFrame(root, text="Imagen original")
        self.image_container.grid(row=0, column=0, padx=10, pady=10)

        # Crear un label para mostrar la imagen original
        self.image_label = tk.Label(self.image_container)
        self.image_label.grid(row=0, column=0, padx=10, pady=10)

        # Barra de progreso 
        self.progress = tk.IntVar()
        self.progress_bar = ttk.Progressbar(self.image_label, orient="horizontal", length=300, mode="determinate", variable=self.progress)
        self.progress_bar.grid(row=0, column=0, padx=10, pady=10)

        # Configurar la distribución de las columnas y filas
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=1)

    def get_imagen_escalada(self, imagen, max_width, max_height):
        # Convertir de numpy.ndarray a PIL.Image
        imagen_pil = Image.fromarray(cv2.cvtColor(imagen, cv2.COLOR_RGB2RGBA))

        # Obtener dimensiones originales
        width, height = imagen_pil.size
        print(f"Tamaño original: {width}x{height}")
        
        # Calcular la escala manteniendo la relación de aspecto
        ratio = min(max_width / width, max_height / height)
        nuevo_tamano = (int(width * ratio), int(height * ratio))
        
        print(f"Tamaño escalado: {nuevo_tamano[0]}x{nuevo_tamano[1]}")
        
        # Escalar la imagen
        imagen_escalada = imagen_pil.resize((nuevo_tamano[0], nuevo_tamano[1]))

        return imagen_escalada

    def display_image(self, image):
        if image is not None:
            print(f"La imagen procesada es de tipo: {type(image)}")
            
            pil_image = self.get_imagen_escalada(image, 640, 640)
            tk_image = ImageTk.PhotoImage(pil_image)

            print(f"Imagen procesada convertida a formato Tkinter")

            self.image_label.grid(row=0, column=0, padx=10, pady=10, sticky="")
            self.image_label.config(image=tk_image)
            self.image_label.image = tk_image

            # Actualizar el tamaño del Label para que se ajuste al tamaño de la imagen
            self.image_label.config(width=pil_image.width, height=pil_image.height)
        else:
            print("No hay imágenes para mostrar")

    def update_progress_thread(self, progress, finished=False):
        # Se actualiza el progreso en el hilo principal
        self.root.after(0, self.update_progress(progress, finished))     

    def update_progress(self, progress, finished=False):
        if (finished):
            # Limpiar el frame para eliminar la barra de progreso
            for widget in self.image_label.winfo_children():
                widget.destroy()

            # Agrupar los caracteres en carpetas con su nombre para formar alfabeto
            image_folder = ALPHABET_PATH
            self.imageController.agruparService.agrupar(image_folder)

            # Mostrar el alfabeto generado por la imagen
            self.image_loaded_callback()

        else:
            #print(f"Progreso de procesamiento: {progress}")
            self.progress.set(progress)

    

    
    
    





