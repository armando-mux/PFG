import importlib
import platform
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sys

# Verificacion (e instalacion) de las librerias necesarias en los scripts 
# de monitorizacion que no son parte del estándar de python.

librerias_requeridas = [
    "watchdog",  # Para monitoreo de archivos
    "psutil",    # Para monitoreo de hardware
    "pyshark",  # Para monitoreo de red
    "pandas",    # Para manejo de datos
    "matplotlib" # Para graficar
]

for libreria in librerias_requeridas:
    try:
        importlib.import_module(libreria)
        print(f"Libreria {libreria} ya instalada")
    except ImportError:
        print(f"{libreria} no instalada, intentando instalar...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", libreria])
        
        
# Encuentra a partir de la localizacion de este script las localizaciones del resto de scripts.
directorio_script = Path(__file__).resolve().parent

# Construir la ruta a la carpeta log
ruta_log = directorio_script / "logs"

# Verificar si la carpeta log existe, y si no, crearla
ruta_log.mkdir(parents=True, exist_ok=True)

# Detectar el sistema operativo
sistema_operativo = platform.system()

# Construir la ruta a los scripts

# Scrips de windows
script1win = directorio_script / "src" / "network" / "windows" / "network.py"
script2win = directorio_script / "src" / "hw_resources" / "windows" / "resources.py"
script3win = directorio_script / "src" / "directories" / "windows" / "directories_monitor.py"
script4win = directorio_script / "src" / "processes" / "windows" / "processes.py"
script5win = directorio_script / "src" / "processes" / "windows" / "services.py"


# Scripts de linux
script1lin = directorio_script / "src" / "network" / "linux" / "network.py"
script2lin = directorio_script / "src" / "hw_resources" / "linux" / "resources.py"
script3lin = directorio_script / "src" / "directories" / "linux" / "directories_monitor.py"
script4lin = directorio_script / "src" / "processes" / "linux" / "processes.py"
script5lin = directorio_script / "src" / "processes" / "linux" / "services.py"


# Definir los scripts para cada sistema operativo
scripts_windows = [script1win, script2win, script3win, script4win, script5win]
scripts_linux = [script1lin, script2lin, script3lin, script4lin, script5lin]


# Función para ejecutar un script
def ejecutar_script(script):
	try:
		if sistema_operativo == "Windows":
			subprocess.run(["python", script], check=True)
		elif sistema_operativo == "Linux":
			subprocess.run(["python3", script], check=True)
	except subprocess.CalledProcessError as e:
		print(f"Error al ejecutar {script}: {e}")



# Seleccionar los scripts correspondientes
if sistema_operativo == "Windows":
    scripts = scripts_windows
elif sistema_operativo == "Linux":
    scripts = scripts_linux
else:
    print("Sistema operativo no soportado")
    exit(1)


# Ejecutar los scripts simultáneamente

with ThreadPoolExecutor() as executor:
	executor.map(ejecutar_script, scripts)
