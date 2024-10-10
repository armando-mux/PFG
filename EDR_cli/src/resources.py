import psutil
import logging
import time
import socket
name = socket.gethostname()
namelog = 'resources_' + name + '.log'
logging.basicConfig(filename= namelog, level=logging.INFO, format='%(asctime)s: %(message)s')

while True:
    # Obtiene el uso de la CPU
    cpu_percent = psutil.cpu_times_percent(interval=1)
    cpu_simple_percent = psutil.cpu_percent(interval=1)
    
    # Obtiene el uso de la memoria
    memory_info = psutil.virtual_memory()
    result = f'CPU: {cpu_simple_percent} [USER: {cpu_percent[0]} SYSTEM: {cpu_percent[1]} IDLE: {cpu_percent[2]} INTERRUPT: {cpu_percent[3]} DCP: {cpu_percent[4]}]' + f' Uso de memoria: {memory_info.percent}%'
    logging.info(result)
    print(result)
    # Espera un segundo antes de obtener la próxima lectura
    time.sleep(1)