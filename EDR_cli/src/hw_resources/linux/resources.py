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
current_file_name = f"{ruta_log}/{name_base}_{file_counter}.csv"


# Función para crear un nuevo archivo y escribir el encabezado
def create_new_file():
    global current_file_name, file_counter
    current_file_name = f"{ruta_log}{name_base}_{file_counter}.csv"
    with open(current_file_name, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Escribir la cabecera
        writer.writerow([
            "Timestamp", "CPU Total", "CPU User", "CPU Nice", "CPU System", 
            "CPU Idle", "CPU Iowait", "CPU Irq", "CPU SoftIrq", "CPU Steal", 
            "CPU Guest", "CPU Guest nice", 
            "Mem Total", "Mem Available", "Mem Percent", "Mem used", "Mem Free",
            "Mem Active", "Mem Inactive", "Buffers", "Cached", "Shared", "Slab",
            "Swap Total", "Swap Used", "Swap Free", "Swap Percent", "Swap Sin", "Swap Sout",            
            "Disco - Lecturas Completadas", 
            "Disco - Escrituras Completadas"
        ])
    print(f"Nuevo archivo creado: {current_file_name}")


def main():
    # Crea el archivo inicial
    create_new_file()

    while True:
        # Obtiene el uso de la CPU
        cpu_percent = psutil.cpu_times_percent()
        cpu_simple_percent = psutil.cpu_percent()
        
        # Obtiene el uso de la memoria
        memory_info = psutil.virtual_memory()
        swap_info = psutil.swap_memory()
        # Obtiene el número de operaciones de disco
        disk_info = psutil.disk_io_counters(perdisk=False, nowrap=False)
        
        # Recopila los datos a registrar
        data_row = [
            time.strftime("%Y-%m-%d %H:%M:%S"),  # Timestamp
            cpu_simple_percent,
            cpu_percent.user, cpu_percent.nice, cpu_percent.system, cpu_percent.idle, 
            cpu_percent.iowait, cpu_percent.irq, cpu_percent.softirq, cpu_percent.steal, 
            cpu_percent.guest, cpu_percent.guest_nice,
            memory_info.total, memory_info.available, memory_info.percent, memory_info.used,
            memory_info.free, memory_info.active, memory_info.inactive, memory_info.buffers, 
            memory_info.cached, memory_info.shared, memory_info.slab,
            swap_info.total, swap_info.used, swap_info.free, swap_info.percent, swap_info.sin, swap_info.sout,
            disk_info.read_count, disk_info.write_count
        ]
        
        # Verifica el tamaño del archivo antes de escribir
        if os.path.exists(current_file_name) and os.path.getsize(current_file_name) > max_file_size:
            print(f"El archivo {current_file_name} ha alcanzado el tamaño máximo permitido.")
            file_counter =+ 1
            create_new_file()
        
        # Escribe los datos en el archivo actual
        with open(current_file_name, mode='a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data_row)

        # Espera un segundo antes de la próxima iteración
        time.sleep(0.5)

if __name__ == "__main__":
    main()