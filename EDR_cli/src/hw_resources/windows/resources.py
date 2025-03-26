from pathlib import Path
import time
import psutil
import csv
import os

# Directorio y nombre base del archivo de registro
name_base = "HW_resources"
ruta_log = Path(__file__).resolve().parent.parent.parent.parent / "logs" 
if not os.path.exists(ruta_log):
    os.makedirs(ruta_log)
file_counter = 0


# Tamaño máximo permitido del archivo en bytes (10 MB)
max_file_size = 10 * 1024 * 1024
current_file_name = f"{ruta_log}\\{name_base}_{file_counter}.csv"


# Función para crear un nuevo archivo y escribir el encabezado
def create_new_file():
    global current_file_name, file_counter
    current_file_name = f"{ruta_log}\\{name_base}_{file_counter}.csv"
    with open(current_file_name, mode='a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Escribir la cabecera
        writer.writerow([
            "Timestamp", "CPU Total (%)", "CPU User (%)", "CPU System (%)", 
            "CPU Idle (%)", "CPU Interrupt (%)", "CPU DCP (%)",
            "Mem Total", "Mem Available", "Mem Percent", "Mem used", "Mem Free",
            "Swap Total", "Swap Used", "Swap Free", "Swap Percent", "Swap Sin", "Swap Sout",
            "Disco - Lecturas Completadas", 
            "Disco - Escrituras Completadas"
        ])
    print(f"Nuevo archivo creado: {current_file_name}")




def main():
    
    create_new_file()
    
    while True:
        # Obtiene el uso de la CPU
        cpu_percent = psutil.cpu_times_percent()
        cpu_simple_percent = psutil.cpu_percent()
    
        # Obtiene el uso de la memoria
        memory_info = psutil.virtual_memory()
        swap_memory = psutil.swap_memory()
    
        # Obtiene el número de operaciones de disco
        disk_info = psutil.disk_io_counters(perdisk=False, nowrap=False)
    
        # Recopila los datos a registrar
        data_row = [
            time.strftime("%Y-%m-%d %H:%M:%S"),  # Timestamp
            cpu_simple_percent, cpu_percent.user, cpu_percent.system, cpu_percent.idle, cpu_percent.interrupt, cpu_percent.dpc, 
            memory_info.total, memory_info.available, memory_info.percent, memory_info.used, memory_info.free, 
            swap_memory.total, swap_memory.used, swap_memory.free, swap_memory.percent, swap_memory.sin, swap_memory.sout,
            disk_info.read_count, disk_info.write_count
        ]
    
        # Verifica el tamaño del archivo antes de escribir (FUNCIONALIDAD DESHABILITADA TEMPORALMENTE)
        # if os.path.exists(current_file_name) and os.path.getsize(current_file_name) > max_file_size:
        #    print(f"El archivo {current_file_name} ha alcanzado el tamaño máximo permitido.")
        #    file_counter += 1
        #    create_new_file()
    
        # Escribe los datos en el archivo actual
        with open(current_file_name, mode='a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data_row)

        # Espera un segundo antes de la próxima iteración
        time.sleep(1)
        
        
if __name__ == "__main__":
    main()
