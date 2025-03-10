import re
import subprocess
import pyshark
import os
import csv

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
            port_src = "N/A"
            port_dst = "N/A"
            transport_protocol = "N/A"
        app_protocol = paquete.highest_layer
        length = paquete.length
    
        paquete_resumen = Paquete(timestamp, ip_src, ip_dst, port_src, port_dst, transport_protocol, app_protocol, length)
        csv_writer.writerow(paquete_resumen.to_row())
        
    except Exception as e:
        print(f"Error: {e}")

def extraer_nombres(lines):
   
    # Expresión regular para extraer el texto entre el punto y el paréntesis
    matches = re.findall(r'\d+\.\s*(.+?)\s*\(', lines)
    return matches

 ## Listar interfaces de red; en Win 'any' no sirve.
def get_interfaces():
    interfaces = subprocess.run("Tshark -D", capture_output=True, text=True).stdout
    resultado = extraer_nombres(interfaces)
    return resultado

def start_capture(output_dir, max_file_size_mb=10):
    os.makedirs(output_dir, exist_ok=True)
    file_index = 0
    outputabsdir = os.path.abspath(output_dir)
    current_file_path = os.path.join(outputabsdir, f"packets_{file_index}.csv")
    print(f"Ruta {current_file_path} creada")
    file_handle = open(current_file_path, mode='w', newline='')
    csv_writer = csv.writer(file_handle)
    
    # Write the header row
    csv_writer.writerow([
        "timestamp", "ip_src", "ip_dst", 
        "port_src", "port_dst", 
        "transport_protocol", "app_protocol", "length"
    ])
    lim = (len(get_interfaces())-1)
    try:
        cap = pyshark.LiveCapture()
        cap.interfaces = get_interfaces()[0:lim]
        for packet in cap.sniff_continuously():
            handle_packet(packet, csv_writer)
            file_handle.flush()  # Ensure data is written to disk
            if os.path.getsize(current_file_path) > max_file_size_mb * 1024 * 1024:
                file_handle.close()
                file_index += 1
                current_file_path = os.path.join(outputabsdir, f"packets_{file_index}.csv")
                file_handle = open(current_file_path, mode='w', newline='')
                csv_writer = csv.writer(file_handle)
                csv_writer.writerow([
                    "timestamp", "ip_src", "ip_dst", 
                    "port_src", "port_dst", 
                    "transport_protocol", "app_protocol", "length"
                ])
    finally:
        file_handle.close()

def main():
    print("Comienza monitoreo")
    start_capture(output_dir="EDR_cli\\logs", max_file_size_mb=10)

if __name__ == "__main__":
    main()
