import csv
import os
from pathlib import Path
from socket import socket
import sys
import pyshark

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
from src import utils

max_file_size = 10 * 1024 
# Clase para representar un paquete de red con métodos de inicializacion, de toString y de conversión a lista para escritura en CSV
class Paquete:
    def __init__ (self, timestamp, ip_src, ip_dst, port_src, port_dst, transport_protocol, app_protocol, length):
        self.timestamp = timestamp
        self.ip_src = ip_src
        self.ip_dst = ip_dst
        self.port_src = port_src
        self.port_dst = port_dst
        self.transport_protocol = transport_protocol
        self.app_protocol = app_protocol
        self.length = length
        
    def __str__(self):
        return f"[{self.timestamp}] {self.transport_protocol} - {self.app_protocol}" + f"  Origen: {self.ip_src}:{self.port_src}" + f"  Destino: {self.ip_dst}:{self.port_dst}" + f"  Longitud: {self.length} bytes\n" 
    
    def to_row(self):
        return [
            self.timestamp.isoformat(),
            self.ip_src,
            self.ip_dst,
            self.port_src,
            self.port_dst,
            self.transport_protocol,
            self.app_protocol,
            self.length
        ] 

# Función para manejar un paquete de red y escribirlo en un archivo CSV
def handle_packet(paquete, csv_writer):
    try: 
        timestamp = paquete.sniff_time
        ip_src = paquete.ip.src if hasattr(paquete, 'ip') else (paquete.ipv6.src if hasattr(paquete, 'ipv6') else "N/A")
        ip_dst = paquete.ip.dst if hasattr(paquete, 'ip') else (paquete.ipv6.dst if hasattr(paquete, 'ipv6') else "N/A")
        if hasattr(paquete, 'transport_layer') and paquete.transport_layer is not None:
            port_src = paquete[paquete.transport_layer].srcport if hasattr(paquete[paquete.transport_layer], 'srcport') else "N/A"
            port_dst = paquete[paquete.transport_layer].dstport if hasattr(paquete[paquete.transport_layer], 'dstport') else "N/A"
            transport_protocol = paquete.transport_layer
        else:
            # Paquetes sin capa de transporte, como ICMP o ARP
            port_src = "N/A"
            port_dst = "N/A"
            transport_protocol = "N/A"
        app_protocol = paquete.highest_layer
        length = paquete.length
    
        paquete_resumen = Paquete(timestamp, ip_src, ip_dst, port_src, port_dst, transport_protocol, app_protocol, length)
        csv_writer.writerow(paquete_resumen.to_row())
        
    except Exception as e:
        print(f"Error: {e}")
        
        
# Función para iniciar la captura de paquetes de red y escribirlos en archivos CSV
def start_capture(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    file_index = 0
    outputabsdir = os.path.abspath(output_dir)
    current_file_path = os.path.join(outputabsdir, f"packets_{file_index}.csv")
    csv_name = f"{socket.gethostname()}/NETWORK/network_data{file_index}.csv"
    print(f"Ruta {current_file_path} creada")
    file_handle = open(current_file_path, mode='w', newline='')
    csv_writer = csv.writer(file_handle)
    csv_writer.writerow([
        "timestamp", "ip_src", "ip_dst", 
        "port_src", "port_dst", 
        "transport_protocol", "app_protocol", "length"
    ])
    try:
        cap = pyshark.LiveCapture(interface='any')
        for packet in cap.sniff_continuously():
            handle_packet(packet, csv_writer)
            file_handle.flush()
            
            if os.path.getsize(current_file_path) > max_file_size :
                utils.send_file(current_file_path, "prueba", csv_name)
                file_handle.close()
                os.remove(current_file_path)
                file_index += 1
                current_file_path = os.path.join(outputabsdir, f"packets_{file_index}.csv")
                file_handle = open(current_file_path, mode='w', newline='')
                csv_name = f"{socket.gethostname()}/NETWORK/network_data{file_index}.csv"
                csv_writer = csv.writer(file_handle)
                csv_writer.writerow([
                    "timestamp", "ip_src", "ip_dst", 
                    "port_src", "port_dst", 
                    "transport_protocol", "app_protocol", "length"
                ])
    except KeyboardInterrupt:
        utils.send_file(current_file_path, "prueba", csv_name)
        file_handle.close()
        cap.eventloop.stop()
        os.remove(current_file_path)

        
        
def main():
    ruta_log = Path(__file__).resolve().parent.parent.parent.parent / "logs"
    start_capture(output_dir=ruta_log)

if __name__ == "__main__":
    main()
