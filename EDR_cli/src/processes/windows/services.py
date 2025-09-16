import os
from pathlib import Path
import socket
import sys
import time
import csv
import psutil
from datetime import datetime
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
from src import utils

# Configuración del archivo CSV
ruta_log = Path(__file__).resolve().parent.parent.parent.parent / "logs" 
header = ["Timestamp", "Nombre", "Estado", "Auto-Start", "PID", "Ruta del ejecutable", "Usuario"]
file_counter = 0
name_base = f"services_{file_counter}.csv"
csv_file = f"{ruta_log}\\{name_base}"
max_file_size = 5 * 1024  # 5 MB

# Obtiene una lista de servicios en ejecución.
def obtener_servicios_en_ejecucion():
    
    servicios_en_ejecucion = []
    for servicio in psutil.win_service_iter():
        servicios_en_ejecucion.append([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Timestamp
            servicio.name(),                                # Nombre del servicio
            #servicio.display_name(),                       # Nombre para mostrar
            servicio.status(),                             # Estado del servicio
            servicio.start_type(),                         # Tipo de inicio
            servicio.pid(),                                # PID del servicio
            servicio.binpath(),                            # Ruta del ejecutable
            servicio.username()                            # Usuario que ejecuta el servicio
        ])
    return servicios_en_ejecucion

# Monitorea los servicios en ejecución y los registra en un archivo CSV.
def monitorear_servicios():
    global csv_file, file_counter, name_base
    print("Iniciando monitoreo de servicios con psutil...")
    try:
        while True:
            with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                if file.tell() == 0:  # Escribe el encabezado si el archivo está vacío
                    writer.writerow(header)

                while not (os.path.exists(csv_file) and os.path.getsize(csv_file) > max_file_size):
                    servicios = obtener_servicios_en_ejecucion()
                    writer.writerows(servicios)  # Escribe todos los servicios en el CSV
                    time.sleep(5)  
            name = socket.gethostname()
            nombre_1 = f"{name}/SERVICES/{name_base}"
            utils.send_file(csv_file, "prueba", nombre_1)
            os.remove(csv_file)
            file_counter += 1
            name_base = f"services_{file_counter}.csv"
            csv_file = f"{ruta_log}/{name_base}"   
    except KeyboardInterrupt:
        name = socket.gethostname()
        nombre_1 = f"{name}/SERVICES/{name_base}"
        utils.send_file(csv_file, "prueba", nombre_1)
        os.remove(csv_file)
           
if __name__ == "__main__":
    monitorear_servicios()  # Intervalo de 10 segundos