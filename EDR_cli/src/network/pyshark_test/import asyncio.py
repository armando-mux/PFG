import threading
import pyshark
import subprocess
import re

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
        self.interface = interface
        
    def __str__(self):
        return f"[{self.timestamp}] {self.transport_protocol} - {self.app_protocol}" + f"  Origen: {self.ip_src}:{self.port_src}" + f"  Destino: {self.ip_dst}:{self.port_dst}" + f"  Longitud: {self.length} bytes\n" + f"  Interfaz: {self.interface}"
    
    
        
class Monitor:
    def __init__ (self, interfaz):
        self.interfaz = interfaz      
        self._stop_event = threading.Event()
        
        
    def sniff_packets(self):
        """Método síncrono para capturar paquetes en la interfaz."""
        capture = pyshark.LiveCapture(interface=self.interfaz)
        print(f"Captura en la interfaz {self.interfaz} iniciada")
        try:
            for packet in capture.sniff_continuously(packet_count=0):
                # Verifica si el evento de parada está activado
                if self._stop_event.is_set():
                    break
                handle_packet(packet, self.interfaz)
        except Exception as e:
            print(f"Error en la captura de {self.interfaz}: {e}")
        finally:
            print(f"Captura detenida en {self.interfaz}")      
            
             
    def start(self):
        """Inicia la captura de paquetes en un hilo separado."""
        self.thread = threading.Thread(target=self.sniff_packets, daemon=True)
        self.thread.start()    
    
    def stop(self):
        """Detiene la captura de paquetes."""
        self._stop_event.set()  # Señala que el hilo debe detenerse
        self.thread.join()      # Espera a que el hilo termine
    
def extraer_nombres(lines):
   
    # Expresión regular para extraer el texto entre el punto y el paréntesis
    matches = re.findall(r'\d+\.\s*(.+?)\s*\(', lines)
    return matches

 ## Listar interfaces de red; en Win 'any' no sirve.
def get_interfaces():
    interfaces = subprocess.run("Tshark -D", capture_output=True, text=True).stdout
    resultado = extraer_nombres(interfaces)
    return resultado
    
## extraer informacion de cada paquete dentro de la captura en vivo
def handle_packet(paquete):
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
        print(f"{paquete_resumen}")
    except Exception as e:
        print(f"Error: {e}")
        


if __name__ == "__main__":
    interfaces = get_interfaces()
    interfaces = interfaces[4:5]
    cap = pyshark.LiveCapture()
    cap.interfaces = ["\\Device\\NPF_{F0A73EDF-FF6E-4CE9-B594-03DA7816414B}", "\\Device\\NPF_{6BE41B42-7AA5-4D36-8798-A0EC8B841982}"]
    for packet in cap.sniff_continuously():
        handle_packet(paquete=packet)
    ##monitores = [Monitor(interfaz) for interfaz in interfaces]
    ##program = [monitor.start() for monitor in monitores]
    