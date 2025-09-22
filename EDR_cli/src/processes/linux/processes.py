import os
import psutil
import time
import csv
from datetime import datetime
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
from src import utils


# Configuración del archivo CSV
ruta_log = Path(__file__).resolve().parent.parent.parent.parent / "logs" 
file_counter = 0
max_file_size = 2 * 1024 
header = ["Timestamp", "PID", "Nombre", "Ruta", "Usuario", "Tiempo de creación", "Proceso padre",
          "Numero lecturas", "Bytes leidos", "Numero escrituras", "Bytes escritos"]

base_name = f"process_monitor{file_counter}.csv"
csv_file = f"{ruta_log}/{base_name}"

# Obtiene la información de un proceso y del proceso padre (si lo hay).
def get_process_info(pid):
    try:
        proc = psutil.Process(pid)
        parent = proc.parent()  # Obtiene el proceso padre
        parent_info = f"{parent.pid} ({parent.name()})" if parent else "N/A"
        return [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            pid,
            proc.name(),
            proc.exe(),
            proc.username(),
            datetime.fromtimestamp(proc.create_time()).strftime("%Y-%m-%d %H:%M:%S"),
            parent_info,
            proc.io_counters().read_count,
            proc.io_counters().read_bytes,
            proc.io_counters().write_count,
            proc.io_counters().write_bytes,

        ]
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return None


# Registra en el archivo CSV todos los procesos activos.
def log_all_processes(writer):
        for proc in psutil.process_iter():
            process_info = get_process_info(proc.pid)
            if process_info:
                writer.writerow(process_info)


# Monitorea y registra todos los procesos activos en intervalos de tiempo.
def monitor_processes():
 
    with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(header)
        while os.path.exists(csv_file) and os.path.getsize(csv_file) < max_file_size:
            log_all_processes(writer)
            time.sleep(5)

if __name__ == "__main__":
    try:
        monitor_processes()
        while True:
            utils.send_file(csv_file, "prueba", f"{base_name}")
            os.remove(csv_file)
            file_counter += 1
            base_name = f"process_monitor{file_counter}.csv"
            csv_file = f"{ruta_log}/{base_name}" 
            monitor_processes()
            
    except KeyboardInterrupt:
        utils.send_file(csv_file, "prueba", f"{base_name}")
        os.remove(csv_file)
        print("Monitoreo de procesos detenido.")