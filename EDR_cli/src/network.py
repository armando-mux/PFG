import subprocess
import logging
import socket
import time

# Configura el logging
name = socket.gethostname()
namelog = 'netstat_' + name + '.log'
logging.basicConfig(filename= namelog, level=logging.INFO, format='%(asctime)s: %(message)s')

while True:
    # Ejecuta el comando netstat
    result = subprocess.run(['netstat', '-n'], capture_output=True, text=True)

    # Almacena el resultado en el log
    logging.info(result.stdout)
    print(result.stdout)

    # Espera 5 segundos antes de ejecutar el comando de nuevo
    time.sleep(5)
