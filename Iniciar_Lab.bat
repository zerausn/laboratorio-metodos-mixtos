@echo off
echo ===================================================
echo Iniciando el Laboratorio de Investigacion (SocEnv Lab)
echo ===================================================
echo.

:: Cambiar al directorio donde esta el script (la carpeta del proyecto)
cd /d "%~dp0"

:: Activar el entorno virtual e iniciar Streamlit
call .\.venv\Scripts\activate.bat
if errorlevel 1 (
    echo Error: No se pudo activar el entorno virtual.
    pause
    exit /b
)

echo Abriendo el navegador...
python -m streamlit run app.py

pause
