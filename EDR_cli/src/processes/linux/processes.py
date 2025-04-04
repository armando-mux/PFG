import psutil
import time
import csv
from datetime import datetime
from pathlib import Path

# Configuración del archivo CSV
ruta_log = Path(__file__).resolve().parent.parent.parent.parent / "logs" 

header = ["Timestamp", "PID", "Nombre", "Ruta", "Usuario", "Tiempo de creación", "Proceso padre",
          "Numero lecturas", "Bytes leidos", "Numero escrituras", "Bytes escritos"]

csv_file = f"{ruta_log}/process_monitor.csv"

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
    print("Iniciando monitoreo de procesos...")
    with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(header)
        while True:
            log_all_processes(writer)
            time.sleep(5)

if __name__ == "__main__":
    try:
        monitor_processes()
    except KeyboardInterrupt:
        print("Monitoreo de procesos detenido.")