import subprocess
import pyshark
import re
import asyncio


def extraer_nombres(lines):
   
    # Expresión regular para extraer el texto entre el punto y el paréntesis
    match = re.findall(r'\d+\.\s*(.+?)\s*\(', lines)
    return match
    


 ## Listar interfaces de red; en Win 'any' no sirve.
def get_interfaces():
    interfaces = subprocess.run("Tshark -D", capture_output=True, text=True).stdout
    resultado = extraer_nombres(interfaces)
    return resultado
    
    
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

    
    
## loop de captura en vivo de una interfaz
async def capturar_paquetes(interfaz):
    try:
       captura = pyshark.LiveCapture(interface=interfaz)
       print(f"Capturando paquetes en interfaz {interfaz} ... Presiona Ctrl+C para detener.")

       # Ejecuta la captura en un hilo separado
       await asyncio.to_thread(iterar_paquetes, captura)

    except KeyboardInterrupt:
        print("\nCaptura detenida por el usuario.")

    except Exception as e:
        print(f"Error: {e}")
        
        
def iterar_paquetes(captura):
    for paquete in captura.sniff_continuously():
        handle_packet(paquete)

# Metodo para iniciar el monitoreo de todas las interfaces.

async def monitoreo():
    interfaces = get_interfaces()
    tareas = [capturar_paquetes(interfaz) for interfaz in interfaces]
    await asyncio.gather(*tareas)

## main
if __name__ == "__main__":
    try:
        asyncio.run(monitoreo())  # Inicia el bucle de eventos asyncio y ejecuta la función `monitoreo`
    except KeyboardInterrupt:
        print("\nMonitoreo detenido por el usuario.")
