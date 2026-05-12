@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

set "PYTHON_EXE=%SCRIPT_DIR%.venv\Scripts\python.exe"
set "APP_SCRIPT=%SCRIPT_DIR%main_v2.py"
set "LOG_DIR=%TEMP%"
set "TV_ROTATION_INTERVAL=40"
set "TV_FIRST_PAGE_ZOOM=0.9"
for /f %%I in ('powershell -NoProfile -Command "(Get-Date).ToString('yyyyMMdd_HHmmss')"') do set "RUN_TIMESTAMP=%%I"
set "STDOUT_LOG=%LOG_DIR%\tv_rotator_stdout_%RUN_TIMESTAMP%.log"
set "STDERR_LOG=%LOG_DIR%\tv_rotator_stderr_%RUN_TIMESTAMP%.log"

rem Limpia logs anteriores a 7 dias para evitar crecimiento indefinido.
powershell -NoProfile -Command ^
  "Get-ChildItem -Path $env:TEMP -Filter 'tv_rotator_*.log' -ErrorAction SilentlyContinue | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-7) } | Remove-Item -Force -ErrorAction SilentlyContinue" >nul 2>&1

if not exist "%PYTHON_EXE%" (
    echo No se encontro el entorno virtual en "%PYTHON_EXE%".>>"%STDERR_LOG%"
    exit /b 1
)

if not exist "%APP_SCRIPT%" (
    echo No se encontro el script principal en "%APP_SCRIPT%".>>"%STDERR_LOG%"
    exit /b 1
)

"%PYTHON_EXE%" "%APP_SCRIPT%" >>"%STDOUT_LOG%" 2>>"%STDERR_LOG%"
exit /b %errorlevel%
