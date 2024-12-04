import time
import psutil
import csv

# Archivo de registro
print("Nombre del archivo con los log de rendimiento: ")
name = input()
path = ".\\EDR_cli\\src\\test_recursos\\"
namelog = path + name + ".csv"
print(namelog)

# Configuración inicial del archivo CSV
with open(namelog, mode='w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Escribir la cabecera
    writer.writerow([
        "Timestamp", "CPU Total (%)", "CPU User (%)", "CPU System (%)", 
        "CPU Idle (%)", "CPU Interrupt (%)", "CPU DCP (%)",
        "Memoria (%)", "Disco - Lecturas Completadas", 
        "Disco - Escrituras Completadas"
    ])

# Tiempo límite de ejecución (en segundos)
tiempo_limite = 30
tiempo_inicio = time.time()  # Marca el inicio del tiempo

while True:
    # Calcula el tiempo transcurrido
    tiempo_transcurrido = time.time() - tiempo_inicio
    if tiempo_transcurrido > tiempo_limite:
        print("Tiempo límite alcanzado. Finalizando registro.")
        break

    # Obtiene el uso de la CPU
    cpu_percent = psutil.cpu_times_percent()
    cpu_simple_percent = psutil.cpu_percent()
    
    # Obtiene el uso de la memoria
    memory_info = psutil.virtual_memory()
    
    # Obtiene el número de operaciones de disco
    disk_info = psutil.disk_io_counters(perdisk=False, nowrap=False)
    
    # Recopila los datos a registrar
    data_row = [
        time.strftime("%Y-%m-%d %H:%M:%S"),  # Timestamp
        cpu_simple_percent,
        cpu_percent.user, cpu_percent.system, cpu_percent.idle, 
        cpu_percent.interrupt, cpu_percent.dpc,
        memory_info.percent,
        disk_info.read_count, disk_info.write_count
    ]
    
    # Escribe los datos en el archivo CSV
    with open(namelog, mode='a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data_row)
    
    # También imprime los datos para referencia
    print(f"Datos registrados: {data_row}")

    # Espera un segundo antes de la próxima iteración
    time.sleep(0.1)
    
