import subprocess
import pyshark


 ## Listar interfaces de red; en Win 'any' no sirve.
def get_interfaces():
    interfaces = subprocess.run("Tshark -D", capture_output=True, text=True).stdout
   
    
## extraer informacion de cada paquete dentro de la captura en vivo
def handle_packet(paquete):
    timestamp = paquete.sniff_time
    ip_src = paquete.ip.src if hasattr(paquete, 'ip') else (paquete.ipv6.src if hasattr(paquete, 'ipv6') else "N/A")
    ip_dst = paquete.ip.dst if hasattr(paquete, 'ip') else (paquete.ipv6.dst if hasattr(paquete, 'ipv6') else "N/A")
    port_src = paquete[paquete.transport_layer].srcport if hasattr(paquete, 'transport_layer') else "N/A"
    port_dst = paquete[paquete.transport_layer].dstport if hasattr(paquete, 'transport_layer') else "N/A"
    transport_protocol = paquete.transport_layer if hasattr(paquete, 'transport_layer') else "N/A"
    app_protocol = paquete.highest_layer
    length = paquete.length
    
    print(f"[{timestamp}] {transport_protocol} - {app_protocol}")
    print(f"  Origen: {ip_src}:{port_src}")
    print(f"  Destino: {ip_dst}:{port_dst}")
    print(f"  Longitud: {length} bytes\n")

    
## loop de captura en vivo
def capturar_paquetes():
    try:
        # Captura en vivo de todas las interfaces
        captura = pyshark.LiveCapture(interface="\\Device\\NPF_{F0A73EDF-FF6E-4CE9-B594-03DA7816414B}")
       
        print("Capturando paquetes... Presiona Ctrl+C para detener.")

        # Iterar sobre cada paquete capturado
        for paquete in captura.sniff_continuously():
            handle_packet(paquete)

    except KeyboardInterrupt:
        print("\nCaptura detenida por el usuario.")

    except Exception as e:
        print(f"Error: {e}")


## main
if __name__ == "__main__":
    capturar_paquetes()
