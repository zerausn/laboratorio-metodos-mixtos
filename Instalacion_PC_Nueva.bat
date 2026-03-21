@echo off
echo =========================================================
echo INSTALADOR DEL LABORATORIO DE INVESTIGACION (SocEnv Lab)
echo =========================================================
echo.
echo Este script creara un entorno virtual nuevo e instalara
echo todas las librerias y el ecosistema de IA necesario.
echo.
echo Requisitos Previos:
echo 1. Tener instalado Python 3.10 o superior (y anadido al PATH).
echo.
pause

:: Cambiar al directorio del script
cd /d "%~dp0"

echo [1/4] Comprobando Python...
python --version
if errorlevel 1 (
    echo Error: Python no esta instalado o no esta en el PATH de Windows.
    echo Por favor instala python desde python.org y vuelve a intentarlo.
    pause
    exit /b
)

echo.
echo [2/4] Creando el Entorno Virtual Seguro (.venv)...
python -m venv .venv

echo.
echo [3/4] Activando entorno y actualizando gestor de paquetes (pip)...
call .\.venv\Scripts\activate.bat
python -m pip install --upgrade pip

echo.
echo [4/4] Instalando el Ecosistema Completo (Librerias de IA, GIS y Estadistica)...
echo Esto puede tardar varios minutos dependiendo de tu conexion a internet.
echo Estamos descargando modelos como Torch, Spacy, PyMuPDF, Whisper, etc.
echo.
pip install -r requirements.txt

echo.
echo Descargando modelo base de lenguaje en Espanol (Spacy)...
python -m spacy download es_core_news_sm

echo.
echo =========================================================
echo ¡INSTALACION BASE COMPLETADA CON EXITO!
echo =========================================================
echo.
echo Notas Adicionales:
echo - Recuerda instalar R y FFMPEG manualmente usando los instaladores 
echo   oficiales si deseas habilitar los modulos estadisticos y la transcripcion
echo   de audios. (Mas info en el README).
echo.
echo Para abrir el laboratorio simplemente haz doble clic en 
echo "Iniciar_Lab.bat" de ahora en adelante.
echo.
pause
