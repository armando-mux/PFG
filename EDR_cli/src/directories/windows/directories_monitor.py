import datetime
import os
from pathlib import Path
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import csv
import re



# Función para inicializar el archivo de registro CSV
def initialize_csv_file(csv_file):
    if not os.path.exists(csv_file):
        with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Time", "Event", "Path src", "Path Dst", "Archive", "isDirectory"])

# Clase para manejar los eventos del sistema de archivos y registrarlos
class CustomEventHandler(FileSystemEventHandler):
    
    def __init__(self, csv_file, excluded_path):
        self.csv_file = csv_file
        self.excluded_path = excluded_path
        self.buffer = []
        self.buffer_size = 100 
    
    def write_buffer(self, buffer):
        with open(self.csv_file, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(buffer)
        self.buffer.clear()
        
    def is_excluded(self, path):
        return any(re.match(pattern, path) for pattern in self.excluded_path)

        
    def log_event(self, isdirectory, event_type, src_path, dest_path=""):
        file_name = os.path.basename(src_path)  # Obtener solo el nombre del archivo
        date_time = datetime.datetime.now().strftime("%Y-%m-%d,%H:%M:%S").split(",")  # Obtener fecha y hora
        if (len(self.buffer) < self.buffer_size):
            self.buffer.append([date_time[0], date_time[1], event_type, src_path, dest_path, file_name, isdirectory])
            print(len(self.buffer))
        if (len(self.buffer) == self.buffer_size):
            self.write_buffer(self.buffer)  
            print("Buffer written to CSV")

    def on_modified(self, event):
        if not self.is_excluded(event.src_path):
            self.log_event(event.is_directory, "MODIFIED", event.src_path)

    def on_created(self, event):
        if not self.is_excluded(event.src_path):
            self.log_event(event.is_directory, "CREATED", event.src_path)

    def on_deleted(self, event):
        if not self.is_excluded(event.src_path):
            self.log_event(event.is_directory, "DELETED", event.src_path)
        
    def on_moved(self, event):
        if not self.is_excluded(event.src_path):
            self.log_event(event.is_directory, "MOVED", event.src_path, event.dest_path)  

def main():
    
    # Path del archivo de registro
    ruta_log = Path(__file__).resolve().parent.parent.parent.parent / "logs" 
    csv_file = f"{ruta_log}/filesystem_event.csv"
    
    # Paths a monitorear
    paths = ["C:\\Users", 
             "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\", 
             "C:\\Windows",
             ]

    
    # Directorio a excluir, el de este mismo programa (sino se crea bucle infinito)
    patron_exclusion0 = re.compile(re.escape(str(ruta_log.parent.parent.parent)))
    patron_exclusion1 = re.compile(r"C:\\Users\\[^\\]+\\AppData\\Local\\(?!Windows\\Explorer\\).*", re.IGNORECASE)
    
    excluded = [patron_exclusion0, patron_exclusion1]       
    
    initialize_csv_file(csv_file)
    
    event_handler = CustomEventHandler(csv_file, excluded)
    observer = Observer()

    # Bucle para monitorear los paths
    for path in paths:
        observer.schedule(event_handler, path, recursive=True)

    try:
        observer.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        event_handler.write_buffer(event_handler.buffer)
    observer.join()


if __name__ == "__main__":
    main()