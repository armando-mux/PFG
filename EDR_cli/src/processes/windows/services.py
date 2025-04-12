from pathlib import Path
import time
import csv
import psutil
from datetime import datetime

# Configuración del archivo CSV
ruta_log = Path(__file__).resolve().parent.parent.parent.parent / "logs" 
header = ["Timestamp", "Nombre", "Estado", "Auto-Start", "PID", "Ruta del ejecutable", "Usuario"]
csv_file = f"{ruta_log}\\services_monitor.csv"

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
   
    print("Iniciando monitoreo de servicios con psutil...")
    with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if file.tell() == 0:  # Escribe el encabezado si el archivo está vacío
            writer.writerow(header)

        while True:
            servicios = obtener_servicios_en_ejecucion()
            writer.writerows(servicios)  # Escribe todos los servicios en el CSV
            time.sleep(600)  

if __name__ == "__main__":
    try:
        monitorear_servicios()  # Intervalo de 10 segundos
    except KeyboardInterrupt:
        print("Monitoreo detenido.")