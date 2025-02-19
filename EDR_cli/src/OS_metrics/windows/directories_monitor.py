import datetime
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import csv


CSV_FILE = "filesystem_event.csv"

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Time", "Event", "Path src", "Path Dst", "Archive", "isDirectory"])
    

excluded = "C:\\Users\\arman\\Documents\\UNED\\PFG\\Pydev"

class CustomEventHandler(FileSystemEventHandler):
    
    def log_event(self, isdirectory, event_type, src_path, dest_path=""):
        file_name = os.path.basename(src_path)  # Obtener solo el nombre del archivo
        date_time = datetime.datetime.now().strftime("%Y-%m-%d,%H:%M:%S").split(",")  # Obtener fecha y hora

        with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([date_time[0], date_time[1], event_type, src_path, dest_path, file_name, isdirectory])
        
    def on_modified(self, event):
        if not(event.src_path.startswith(excluded)):
            self.log_event(event.is_directory, "MODIFIED", event.src_path)

    def on_created(self, event):
        self.log_event(event.is_directory, "CREATED", event.src_path)

    def on_deleted(self, event):
        self.log_event(event.is_directory, "DELETED", event.src_path)
        
    def on_moved(self, event):
        self.log_event(event.is_directory, "MOVED", event.src_path, event.dest_path)  

paths = ["C:\\Users", "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\", "C:\\Windows\\System32\\", 
         "C:\\Windows\\System32\\", "C:\\Windows\\SysWOW64\\", "C:\\Windows\\Temp\\", "C:\\Windows\\Tasks\\"]

event_handler = CustomEventHandler()
observer = Observer()

for path in paths:
    observer.schedule(event_handler, path, recursive=True)

try:
    observer.start()
    while True:
        time.sleep(1)  # Mantén el proceso corriendo
except KeyboardInterrupt:
    observer.stop()
observer.join()
