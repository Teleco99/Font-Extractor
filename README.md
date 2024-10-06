# Font-Extractor
Font Extractor es una aplicación en Python diseñada para extraer fuentes tipográficas directamente desde imágenes de documentos. Utilizando tecnologías avanzadas de procesamiento de imágenes y reconocimiento óptico de caracteres (OCR), esta herramienta identifica y procesa fuentes tipográficas presentes en los documentos y las exporta en formatos utilizables.

### Características:
- Extracción precisa de fuentes desde imágenes de documentos escaneados.
- Exportación de fuentes en los formatos OTF (OpenType Font) y SDF (Signed Distance Field).
- Procesamiento eficiente de múltiples caracteres y estilos tipográficos.
### Uso:
1. Cargar la imagen del documento desde 'Archivo'->'Abrir archivo'.
2. Crear el alfabeto a partir de los contornos de la imagen.
3. Generar los archivos SVGs para formar la fuente desde 'proyecto'->'Generar SVGs'.
4. Guardar las fuentes extraídas (OTF y SDF) desde 'Proyecto'->'Generar fuente'.

El proyecto se encuentra en una versión muy temprana e inestable, solo se ha testeado el flujo principal de la aplicación.

## Instalación

### Requisitos:
- Windows
- Python 3.8 o superior
- Tesseract OCR
- FontForge

### Pasos de instalación:

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/image-font-extractor.git
   cd image-font-extractor
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Añade al PATH de tu sistema los binarios de FontForge:
   
   Por defecto la ruta que se debe añadir al PATH es 'C:\Program Files (x86)\FontForgeBuilds\bin'. Esto dependerá de donde se encuentre instalado FontForge.
   
5. Configura la ruta de Tesseract editando 'constant.py':
   ```python
   TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe' # Ruta por defecto
   ```
6. Ejecuta el script principal para iniciar el programa:
   ```bash
   python main.py
   ```
    
