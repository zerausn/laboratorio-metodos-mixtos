===============================================================
GUIA DE INSTALACION PARA EL LABORATORIO EN UN NUEVO PC
===============================================================

Para llevar y configurar todo este avanzado ecosistema de investigación a 
la computadora de un colega, la universidad o un nuevo equipo propio, 
deberás seguir únicamente estos 4 pasos maestros:

---------------------------------------------------------------
PASO 1: LLEVAR LA CARPETA
---------------------------------------------------------------
1. Copia toda esta carpeta (`research_lab`) en una memoria USB o disco duro.
2. (MUY IMPORTANTE): Antes de copiarla, asegúrate de NO copiar la carpeta 
   llamada ".venv" que está oculta adentro. Esa carpeta es única de tu PC 
   actual y pesará gigabytes. Solo te interesa llevarte los archivos 
   .py, .txt y tus reportes/workspaces.

---------------------------------------------------------------
PASO 2: LOS PROGRAMAS BASE DEL SISTEMA (Requisito)
---------------------------------------------------------------
En la nueva computadora asegúrate de que existen estos Softwares Base.
Si no están, descárgalos e instálalos usando sus instaladores "Siguiente->Siguiente":

a) Python (El Motor Principal): 
   Descarga e instala Python 3.10 o posterior desde python.org. 
   **CLAVE:** Al momento de instalarlo (en la primera pantalla), asegúrate de 
   marcar la casilla que dice "Add Python.exe to PATH".

b) R (Para la Estadística Mixta avanzada):
   Si usarás el módulo R, descarga e instala "R Project" desde r-project.org.

c) FFMPEG (Para transcripción Automática de Whisper):
   Si vas a usar el motor de Inteligencia Artificial para desgrabar audios, 
   Windows requiere que instales FFMPEG (es vital para el formato mp3):
   - Descarga FFMPEG compilado para Windows.
   - Extrae la carpeta y añade la carpeta `/bin` a las variables de Entorno PATH 
     de Windows (hay muchos tutoriales simples en Youtube de "Cómo instalar ffmpeg windows").

---------------------------------------------------------------
PASO 3: INSTALACION AUTOMATICA (El Botón Mágico)
---------------------------------------------------------------
1. Ya con Python correctamente instalado, ve a la carpeta del Laboratorio.
2. Haz doble clic en el archivo llamado: **`Instalacion_PC_Nueva.bat`**
3. ¡No hagas nada! Verás una pantalla negra como de "Matrix" empezar a 
   crear un entorno completamente nuevo (un `.venv` limpio) y comenzará 
   a descargar todas las librerías científicas, NLP, geográficas y modelos matemáticos.
   (Tomará su tiempo, ten paciencia).

---------------------------------------------------------------
PASO 4: A INVESTIGAR
---------------------------------------------------------------
1. Cuando la instalación automatizada diga "¡Completado con Éxito!", ya
   podrás cerrar esa ventana.
2. A partir de ahora, solo haces doble clic en **`Iniciar_Lab.bat`**
   (tal cual como lo haces en esta computadora) y el laboratorio florecerá 
   nuevamente en el navegador de la nueva PC, con todos tus workspaces y citas.

===============================================================
¡Éxitos con la investigación!
===============================================================
