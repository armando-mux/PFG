import libpcap
import sys
import socket
import struct

# Definimos el callback para manejar los paquetes capturados
def packet_handler(ts, pkt, pktlen):
    print(f"Paquete capturado - Timestamp: {ts}, Longitud: {pktlen} bytes")
    try:
        # Extraemos la dirección IP de origen y destino si es un paquete IP
        eth_header = struct.unpack("!6s6sH", pkt[0:14])
        eth_proto = socket.ntohs(eth_header[2])

        # Si el protocolo es IP (0x0800), procesamos el paquete
        if eth_proto == 0x0800:
            ip_header = pkt[14:34]
            iph = struct.unpack("!BBHHHBBH4s4s", ip_header)
            src_ip = socket.inet_ntoa(iph[8])
            dst_ip = socket.inet_ntoa(iph[9])
            print(f"IP Origen: {src_ip}, IP Destino: {dst_ip}")
    except Exception as e:
        print(f"Error procesando el paquete: {e}")

# Función principal para iniciar la captura
def main():
    # Verificamos si estamos en Windows o Unix/Linux
    if sys.platform.startswith("win"):
        interface = "\\Device\\NPF_{F0A73EDF-FF6E-4CE9-B594-03DA7816414B}"  # Reemplaza con la interfaz correcta
    else:
        interface = "any"  # Captura de todas las interfaces en Unix/Linux

    print(f"Capturando en la interfaz: {interface}")

    # Iniciamos la captura con libpcap
    pcap = libpcap.pcap(name=interface, promisc=False, timeout_ms=50)
    try:
        # Captura paquetes
        libpcap.dispatch(pcap);
        pcap.loop(0, packet_handler)
    except KeyboardInterrupt:
        print("\nDeteniendo la captura de paquetes")
    finally:
        # Cerramos la captura de paquetes
        libpcap.close(pcap)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nDeteniendo el programa")
