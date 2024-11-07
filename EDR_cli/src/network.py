import signal
import pyshark

# Configura la interfaz de red para la captura en vivo
INTERFACE = 'Wi-Fi'  # Cambia 'Ethernet' al nombre de tu interfaz de red

def show_packet(packet):
    try:
        # Obtiene detalles del paquete
        src_ip = packet.ip.src if hasattr(packet, 'ip') else "N/A"
        dst_ip = packet.ip.dst if hasattr(packet, 'ip') else "N/A"
        protocol = packet.highest_layer  # Protocolo de alto nivel
        length = packet.length  # Tamaño del paquete

        # Muestra la información en la terminal
        print(f"Paquete capturado - Origen: {src_ip}, Destino: {dst_ip}, Protocolo: {protocol}, Tamaño: {length} bytes")
        
    except AttributeError:
        # Algunos paquetes pueden no tener los atributos esperados
        print("Paquete sin datos relevantes, omitiendo...")
        

# Iniciar la captura en vivo en la interfaz especificada
capture = pyshark.LiveCapture(interface=INTERFACE)

print("Iniciando monitoreo de paquetes de red en tiempo real... Presiona Ctrl+C para detener.")
# Procesa cada paquete capturado en tiempo real
capture.apply_on_packets(show_packet)