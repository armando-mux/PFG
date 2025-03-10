import platform
import subprocess
from concurrent.futures import ThreadPoolExecutor

# Definir los scripts para cada sistema operativo
scripts_windows = ["EDR_cli/src/hw_resources/windows/resources.py", "EDR_cli/src/network/windows/test.py", 
                   "EDR_cli/src/OS_metrics/windows/directories_monitor.py"]
scripts_linux = ["/src/hw_resources/linux/resources.py", "./src/network/linux/test.py", 
                 "/src/OS_metrics/linux/directories_monitor.py"]

# Función para ejecutar un script
def ejecutar_script(script):
    try:
        subprocess.run(["python", script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar {script}: {e}")

# Detectar el sistema operativo
sistema_operativo = platform.system()

# Seleccionar los scripts correspondientes
if sistema_operativo == "Windows":
    scripts = scripts_windows
elif sistema_operativo == "Linux":
    scripts = scripts_linux
else:
    print("Sistema operativo no soportado")
    exit(1)

# Ejecutar los scripts simultáneamente usando ThreadPoolExecutor
with ThreadPoolExecutor() as executor:
    executor.map(ejecutar_script, scripts)

print("Todos los scripts han sido ejecutados.")