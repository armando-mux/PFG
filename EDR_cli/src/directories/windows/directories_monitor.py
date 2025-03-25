import datetime
import os
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import csv



# Función para inicializar el archivo de registro CSV
def initialize_csv_file(csv_file):
    if not os.path.exists(csv_file):
        with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Time", "Event", "Path src", "Path Dst", "Archive", "isDirectory"])

# Clase para manejar los eventos del sistema de archivos y registrarlos
class CustomEventHandler(FileSystemEventHandler):
    
    def __init__(self, csv_file, excluded_path):
        self.csv_file = csv_file
        self.excluded_path = excluded_path
    
    def log_event(self, isdirectory, event_type, src_path, dest_path=""):
        file_name = os.path.basename(src_path)  # Obtener solo el nombre del archivo
        date_time = datetime.datetime.now().strftime("%Y-%m-%d,%H:%M:%S").split(",")  # Obtener fecha y hora

        with open(self.csv_file, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([date_time[0], date_time[1], event_type, src_path, dest_path, file_name, isdirectory])
        
    def on_modified(self, event):
        if not any(event.src_path.startswith(excluded) for excluded in self.excluded_path):
            self.log_event(event.is_directory, "MODIFIED", event.src_path)

    def on_created(self, event):
        self.log_event(event.is_directory, "CREATED", event.src_path)

    def on_deleted(self, event):
        self.log_event(event.is_directory, "DELETED", event.src_path)
        
    def on_moved(self, event):
        self.log_event(event.is_directory, "MOVED", event.src_path, event.dest_path)  

def main():
    
    # Path del archivo de registro
    ruta_log = Path(__file__).resolve().parent.parent.parent.parent / "logs" 
    csv_file = f"{ruta_log}/filesystem_event.csv"
    
    # Paths a monitorear
    paths = ["C:\\Users", "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\", 
                "C:\\Windows\\System32\\", "C:\\Windows\\SysWOW64\\", "C:\\Windows\\Temp\\", "C:\\Windows\\Tasks\\"]

    
    # Directorio a excluir, el de este mismo programa (sino se crea bucle infinito)
    excluded = [str(ruta_log.parent.parent.parent)]
    
    initialize_csv_file(csv_file)
    
    event_handler = CustomEventHandler(csv_file, excluded)
    observer = Observer()

    # Bucle para monitorear los paths
    for path in paths:
        observer.schedule(event_handler, path, recursive=True)

    try:
        observer.start()
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()