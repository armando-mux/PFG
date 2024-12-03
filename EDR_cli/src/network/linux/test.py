import re
import subprocess
import pyshark

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

cap = pyshark.LiveCapture(interface='any')
for packet in cap.sniff_continuously():
    handle_packet(packet)
