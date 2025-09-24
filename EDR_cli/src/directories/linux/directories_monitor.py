import datetime
import os
import socket
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import csv
from pathlib import Path
import re
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
from src import utils

file_counter = 0
max_file_size =  15* 1024

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

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
            
        if (len(self.buffer) == self.buffer_size):
            self.write_buffer(self.buffer)  
            

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
    global file_counter, max_file_size, name_base
    
    # Paths a monitorear	
    paths = ["/home/", "/usr/bin/", "/tmp/", "/var/tmp/", "/mnt/", "/opt/"]
    
    # Path del archivo de log
    ruta_log = Path(__file__).resolve().parent.parent.parent.parent / "logs" 
    name_base = f"filesystem_event{file_counter}.csv"
    csv_file = f"{ruta_log}/{name_base}"
    
    # Paths exluidos del monitoreo (bucle infinito)
    excluded = [re.compile(str(ruta_log.parent.parent.parent))]
    
    
    initialize_csv_file(csv_file)
    
    event_handler = CustomEventHandler(csv_file, excluded)
    observer = Observer()
    print("Comenzando monitoreo de directorios")
    # Bucle para monitorear los paths
    for path in paths:
        observer.schedule(event_handler, path, recursive=True)

    try:
        observer.start()
        while True:
            if os.path.exists(csv_file) and os.path.getsize(csv_file) > max_file_size:
                observer.stop()
                event_handler.write_buffer(event_handler.buffer)
                name = socket.gethostname()
                nombre_1 = f"{name}/DIRECTORIES/{name_base}"
                utils.send_file(csv_file, "prueba", nombre_1)
                os.remove(csv_file)
                file_counter += 1
                name_base = f"filesystem_event{file_counter}.csv"
                csv_file = f"{ruta_log}/{name_base}"
                initialize_csv_file(csv_file)
                event_handler = CustomEventHandler(csv_file, excluded)
                observer = Observer()
                for path in paths:
                    observer.schedule(event_handler, path, recursive=True)
                observer.start()
            time.sleep(1)
            
    except KeyboardInterrupt:
        observer.stop()
        event_handler.write_buffer(event_handler.buffer)
        name = socket.gethostname()
        nombre_1 = f"{name}/DIRECTORIES/{name_base}"
        utils.send_file(csv_file, "prueba", nombre_1)
        os.remove(csv_file)
    observer.join()


if __name__ == "__main__":
    main()
