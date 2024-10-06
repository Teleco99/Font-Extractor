from Models.ProyectModel import ProyectModel

class ProyectController:
    def __init__(self):
        self.model = ProyectModel()
        

    def get_alphabet(self, base_folder): 
        return self.model.get_image_paths_by_folder_name(base_folder)
    
    def generar_SVGs(self):
        self.model.generar_vectores(mayuscula=False)
        self.model.generar_vectores(mayuscula=True)

    def generar_OTF(self):
        self.model.generar_fuente()
    
    def set_image_to_letter(self, letra, new_image):
        '''Colocar la imagen seleccionada en la letra indicada actualizando el modelo, 
            esto es necesario ya que al generar la fuente se usa el modelo guardado'''
        
        # Colocar la imagen en la primera posición
        self.model.insert_value_in_list(letra, 0, new_image)

    def add_imagen(self, imagen_path, destino_path):
        self.model.copy_image_to_folder(imagen_path, destino_path)

    def reset_proyecto(self):
        self.model.borrar_carpetas()