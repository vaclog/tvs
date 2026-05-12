# TVS Rotator

Script de rotación de pantallas para TV usando Playwright y Google Chrome en modo kiosco.

## Requisitos

- Windows
- Python 3 instalado y disponible en `PATH`
- Google Chrome instalado

## Archivos principales

- [main_v2.py](./main_v2.py): abre las URLs y rota entre pestañas.
- [requirements.txt](./requirements.txt): dependencias de Python.
- [run_tv_rotator.cmd](./run_tv_rotator.cmd): wrapper para ejecutar desde el Programador de tareas.
- [create_scheduler_task.ps1](./create_scheduler_task.ps1): crea o actualiza la tarea programada en Windows.

## Instalación

1. Abrir PowerShell en la carpeta del proyecto:

```powershell
cd C:\prg\VACLOG\TVS
```

2. Crear el entorno virtual:

```powershell
python -m venv .venv
```

3. Activar el entorno virtual:

```powershell
.venv\Scripts\Activate.ps1
```

4. Instalar dependencias:

```powershell
pip install -r requirements.txt
```

5. Instalar el navegador para Playwright:

```powershell
python -m playwright install chrome
```

## Configuración

Las URLs a mostrar están definidas en [main_v2.py](./main_v2.py).

El navegador está configurado para abrir en modo kiosco real:

- `--kiosk`
- `--start-fullscreen`
- sin barra de notificaciones
- sin infobars de automatización

Actualmente son:

- `https://vots20.vaclog.com/modulos/tv/tableros/tablero_tv.php`
- `https://vots20.vaclog.com/modulos/tv/terminales/terminales_v2.php`
- `https://vots20.vaclog.com/modulos/tv/ofic/ofic.php`

El intervalo de rotación por defecto es de 45 segundos.

Si querés cambiarlo sin editar el código, podés definir la variable de entorno `TV_ROTATION_INTERVAL`.

El zoom de la primera URL (`tablero_tv.php`) también se puede configurar con `TV_FIRST_PAGE_ZOOM`.
En el wrapper [run_tv_rotator.cmd](./run_tv_rotator.cmd) ya quedaron ambas variables listas para editar:

```cmd
set "TV_ROTATION_INTERVAL=45"
set "TV_FIRST_PAGE_ZOOM=0.7"
```

Ejemplo:

```powershell
$env:TV_ROTATION_INTERVAL = "30"
$env:TV_FIRST_PAGE_ZOOM = "0.8"
python main_v2.py
```

## Ejecución manual

Con el entorno virtual activado:

```powershell
python main_v2.py
```

El navegador abrirá Chrome en pantalla completa tipo kiosco y rotará entre pestañas sin recargar.

Para detenerlo:

- presionar `Ctrl+C`

## Ejecución con Programador de tareas

Usar el archivo:

- [run_tv_rotator.cmd](./run_tv_rotator.cmd)
- [create_scheduler_task.ps1](./create_scheduler_task.ps1)

### Opción automática

Ejecutar en PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\create_scheduler_task.ps1
```

Esto crea o actualiza una tarea llamada `TVS Rotator` que:

- se ejecuta al iniciar sesión
- lanza `run_tv_rotator.cmd`
- usa `C:\prg\VACLOG\TVS` como carpeta de trabajo
- ignora inicios duplicados si ya está corriendo
- intenta reiniciar hasta 3 veces si falla

### Opción manual

Configuración recomendada de la tarea:

1. Abrir `taskschd.msc`
2. Crear una tarea nueva
3. En `Desencadenadores`, elegir `Al iniciar sesión`
4. En `Acciones`, configurar:

Programa o script:
```text
C:\prg\VACLOG\TVS\run_tv_rotator.cmd
```

Iniciar en:
```text
C:\prg\VACLOG\TVS
```

## Logs

Cada ejecución genera dos archivos en `%TEMP%`:

- `tv_rotator_stdout_YYYYMMDD_HHMMSS.log`
- `tv_rotator_stderr_YYYYMMDD_HHMMSS.log`

El script elimina automáticamente los logs de más de 7 días.

Para ver la carpeta real de `%TEMP%`:

```powershell
echo $env:TEMP
```

## Problemas comunes

Si falla la activación del entorno virtual en PowerShell por políticas de ejecución:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Si Playwright no encuentra Chrome, volver a ejecutar:

```powershell
python -m playwright install chrome
```

Si querés cambiar las pantallas, editar la lista `URLS` en [main_v2.py](./main_v2.py).
