import tkinter as tk
from Views.ImageView import ImageView
from Views.AlphabetView import AlphabetView
from Controllers.ImageController import ImageController
from Controllers.ProyectController import ProyectController
from constants import ALPHABET_GROUPED_PATH

def image_loaded_callback():
    # Mostrar la imagen procesada
    imageView.display_image(imageController.get_processed_image())
    alphabetView.display_alphabet(ALPHABET_GROUPED_PATH)

if __name__ == "__main__":
    root = tk.Tk()
    imageController = ImageController()
    proyectController = ProyectController()

    # Borrar el proyecto anterior
    proyectController.reset_proyecto()
    
    imageView = ImageView(root, imageController, image_loaded_callback)
    alphabetView = AlphabetView(root, proyectController)
    
    root.geometry("1000x700")
    root.mainloop()


