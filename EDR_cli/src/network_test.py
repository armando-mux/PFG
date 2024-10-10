import pcapy
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, TCP

def procesar_paquete(header, data):
    eth_frame = Ether(data)
    if IP in eth_frame:
        ip_packet = eth_frame[IP]
        if TCP in ip_packet:
            src_ip = ip_packet.src
            dst_ip = ip_packet.dst
            src_port = ip_packet[TCP].sport
            dst_port = ip_packet[TCP].dport
            print(f"Conexión desde {src_ip}:{src_port} a {dst_ip}:{dst_port}")

# Configura la interfaz de red (ajústala según tu caso)
interface = "eth0"

# Abre la interfaz para capturar paquetes
cap = pcapy.open_live(interface, 65536, True, 100)

# Captura paquetes y procesa cada uno
while True:
    (header, data) = cap.next()
    procesar_paquete(header, data)