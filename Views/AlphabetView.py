import tkinter as tk
import os
from PIL import Image, ImageTk
from tkinter import filedialog, Menu
from constants import ALPHABET_GROUPED_PATH, X_PATH

class AlphabetView:
    def __init__(self, root, proyectController):
        self.root = root
        self.proyectController = proyectController
        self.selected_letter = None  # Para saber cuál es la letra seleccionada
        self.selected_letter_label = None  # Almacena el Label de la letra seleccionada en alphabet_frame
        self.selected_image_label = None  # Almacena el Label de la imagen seleccionada en letter_frame
        self.alphabet_labels = {}  # Para mantener referencia a los labels del alfabeto

        self.letras_minusculas = [] 
        self.letras_mayusculas = []
        self.alphabet_actual = self.letras_minusculas

        self.submenu_proyecto = Menu(self.root.menu, tearoff=0)
        self.root.menu.add_cascade(label="Proyecto", menu=self.submenu_proyecto)

        # Opción para generar SVGs de alfabeto
        self.submenu_proyecto.add_command(label="Generar SVGs", command=lambda: self.proyectController.generar_SVGs())

        # Opción para generar fuente OTF
        self.submenu_proyecto.add_command(label="Generar fuente", command=lambda: self.proyectController.generar_OTF())

        # Crear área para mostrar abecedario
        self.alphabet_frame = tk.Frame(root, relief="raised")
        self.alphabet_frame.grid(row=0, column=1, padx=10, pady=10)

        # Crear área para mostrar las imágenes de la letra seleccionada
        self.letter_frame = tk.Frame(root, relief="raised")
        self.letter_frame.grid(row=0, column=2, padx=10, pady=10)

    def display_alphabet(self, base_folder):
        if len(self.alphabet_actual) == 0:
            self.letras_minusculas, self.letras_mayusculas = self.proyectController.get_alphabet(base_folder)
            self.alphabet_actual = self.letras_minusculas

        # Limpiar el contenido previo del frame
        for widget in self.alphabet_frame.winfo_children():
            widget.destroy()

        row = 0
        col = 0

        # Número de caracteres por fila
        max_cols = 10

        for letra, imagenes in self.alphabet_actual.items():
            # Crear un Label para mostrar la imagen o una "X" si no hay imágenes
            if imagenes:
                image_path = imagenes[0]  # Primera imagen de la lista
            else:
                image_path = X_PATH

            img = Image.open(image_path)
            img.thumbnail((100, 100))  # Redimensionar a miniaturas
            tk_image = ImageTk.PhotoImage(img)
                
            label = tk.Label(self.alphabet_frame, image=tk_image, text=letra, compound="top", bg="white")
            label.image = tk_image  # Evitar que la imagen sea recolectada por el GC

            label.grid(row=row, column=col, padx=10, pady=10)
            label.bind("<Button-1>", lambda e, l=letra, letter_label=label: self.show_letter_images(l, letter_label))  # Añadir evento de clic

            # Almacenar el label del alfabeto en el diccionario para referencia posterior
            self.alphabet_labels[letra] = label

            # Actualizar la posición de fila y columna
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

        # Crear el botón en la fila 4, columna 5
        boton_cambiar_mayusculas = tk.Button(self.alphabet_frame, text="Cambiar", command=self.cambiar_alphabet)
        boton_cambiar_mayusculas.grid(row=3, column=4)

    def cambiar_alphabet(self):
        # Cambiar minusculas y mayusculas 
        if self.alphabet_actual == self.letras_mayusculas:
            self.alphabet_actual = self.letras_minusculas
        else:
            self.alphabet_actual = self.letras_mayusculas

        # Resetear las selecciones del usuario
        self.selected_letter = None  # Para saber cuál es la letra seleccionada
        self.selected_letter_label = None  # Almacena el Label de la letra seleccionada en alphabet_frame
        self.selected_image_label = None  # Almacena el Label de la imagen seleccionada en letter_frame

        self.display_alphabet(ALPHABET_GROUPED_PATH)

    def show_letter_images(self, letter, letter_label):
        # Eliminar cualquier imagen previa
        for widget in self.letter_frame.winfo_children():
            widget.destroy()

        # Eliminar posible referencia a imagen antigua
        self.selected_image_label = None

        # Guardar la letra seleccionada y marcarla en alphabet_frame
        self.marcar_letra_seleccionada(letter_label)
        self.selected_letter = letter

        # Crear el botón encima
        boton_add_imagen = tk.Button(self.letter_frame, text="Añadir imagen", command=lambda: self.add_imagen(letter), pady=10)
        boton_add_imagen.grid(row=0, column=1)

        # Cargar las imágenes de la carpeta de la letra seleccionada
        letter_folder = os.path.join(ALPHABET_GROUPED_PATH, letter)
        if os.path.exists(letter_folder):
            image_files = [f for f in os.listdir(letter_folder) if f.endswith(".png")]

            # Mostrar las imágenes en una matriz de 3 columnas
            for idx, image_file in enumerate(image_files):
                image_path = os.path.join(letter_folder, image_file)
                img = Image.open(image_path)
                img.thumbnail((100, 100))  # Redimensionar a miniaturas
                tk_image = ImageTk.PhotoImage(img)

                # Crear un label para mostrar la imagen
                row, col = divmod(idx, 3)
                label = tk.Label(self.letter_frame, image=tk_image, bd=1, relief="solid", bg="white")
                label.grid(row=(row + 1), column=col, ipadx=5, ipady=5)
                label.image = tk_image  # Mantener referencia a la imagen para evitar que sea recolectada por el GC

                # Añadir evento de clic para cambiar la imagen en el alphabet_frame
                label.bind("<Button-1>", lambda e, img_label=label, img_path=image_path: self.cambiar_imagen_alphabet(img_path, img_label))

    def marcar_letra_seleccionada(self, letter_label):
        """Marcar visualmente la letra seleccionada en alphabet_frame."""
        # Desmarcar la letra previamente seleccionada si existe
        if self.selected_letter_label:
            self.selected_letter_label.config(bg="white")

        # Marcar la nueva letra seleccionada
        self.selected_letter_label = letter_label
        self.selected_letter_label.config(bg="green")

        label_position = letter_label.grid_info()
        print(f"Letra marcada: (row, column): ({label_position['row']}, {label_position['column']})")

    def marcar_imagen_seleccionada(self, image_label):
        """Marcar visualmente la imagen seleccionada en letter_frame"""
        if self.selected_image_label:
            self.selected_image_label.config(bg="white")

        self.selected_image_label = image_label
        self.selected_image_label.config(bg="green")

        label_position = image_label.grid_info()
        print(f"Imagen marcada (row, column): ({label_position['row']}, {label_position['column']})")

    def cambiar_imagen_alphabet(self, nueva_imagen, image_label):
        """Cambiar la imagen de la letra seleccionada en alphabet_frame."""
        if self.selected_letter:
            # Cambiar la imagen en el alphabet_frame de la letra seleccionada
            alphabet_label = self.alphabet_labels[self.selected_letter]

            # Insertar la nueva imagen en su lugar
            img = Image.open(nueva_imagen)
            img.thumbnail((100, 100))  # Redimensionar a miniaturas
            img = ImageTk.PhotoImage(img)

            # Actualizar la imagen en el diccionario y en el alphabet_frame
            alphabet_label.config(image=img)
            alphabet_label.image = img

            # Actualizar el diccionario para la generación de la fuente
            self.proyectController.set_image_to_letter(self.selected_letter, nueva_imagen)

            self.marcar_imagen_seleccionada(image_label)
            print(f"Imagen de la letra {self.selected_letter} cambiada")  

    def add_imagen(self, letter):
        # Obtener el directorio actual
        directorio_actual = os.getcwd()

        # Abrir el diálogo para seleccionar un archivo
        image_path = filedialog.askopenfilename(
            initialdir=directorio_actual,
            title="Selecciona una imagen",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.gif *.bmp"), ("Todos los archivos", "*.*")]
        )
        
        # Mostrar la ruta en la terminal
        if image_path:
            # Copiamos imagen a la carpeta de letra seleccionada
            destino_path = os.path.join(ALPHABET_GROUPED_PATH, letter)
            self.proyectController.add_imagen(image_path, destino_path)

            # Cargar la imagen en miniatura
            img = Image.open(image_path)
            img.thumbnail((100, 100))  # Redimensionar a miniatura
            tk_image = ImageTk.PhotoImage(img)

            # Conseguir siguiente posición de la matriz de imagenes
            letter_labels = self.letter_frame.winfo_children() 
            if len(letter_labels) == 1:
                # Si solo esta el boton, se pone en la siguiente fila
                next_column = 0
                next_row = 1
            else:
                last_label = letter_labels[-1]
                column = last_label.grid_info()['column'] 
                row = last_label.grid_info()['row']
                if column < 3:
                    next_column = column + 1  
                    next_row = row
                else:
                    next_column = 0
                    next_row = row + 1

            # Crear el label para la imagen 
            label = tk.Label(self.letter_frame, image=tk_image, bd=1, relief="solid", bg="white")
            label.image = tk_image  # Guardar la referencia para evitar el garbage collector
            label.grid(row=next_row, column=next_column, ipadx=5, ipady=5)

            # Añadir evento de clic para cambiar la imagen en el alphabet_frame
            label.bind("<Button-1>", lambda e, img_label=label, img_path=image_path: self.cambiar_imagen_alphabet(img_path, img_label))

            print(f'Nueva imagen colocada en {next_row, next_column}')
        else:
            print("No se ha seleccionado ningún fichero")