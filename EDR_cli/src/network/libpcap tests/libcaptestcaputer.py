import ctypes
import libpcap

def packet_handler(user_data, header, packet):
    """Función que se llama para procesar los paquetes capturados"""
    print(f"Paquete capturado: longitud del paquete = {header.contents.len} bytes")

def monitor_interface(interfaceName):
    """Monitorea una interfaz de red específica"""
    # Inicializa un buffer de error
    errbuf = ctypes.create_string_buffer(256)
    PCAP_HANDLER_TYPE = ctypes.CFUNCTYPE(None, ctypes.POINTER(libpcap.pkthdr), ctypes.POINTER(ctypes.c_ubyte), ctypes.c_void_p)
    packet_handler_c = PCAP_HANDLER_TYPE(packet_handler)

    # Encuentra la interfaz
    handle = libpcap.open_live(interfaceName.encode('utf-8'), 65535, 0, 1000, errbuf)
    if not handle:
        print(f"Error  {errbuf.value.decode()}")
        return

    # Captura los paquetes
    libpcap.loop(handle, 0, packet_handler_c, None)

if __name__ == "__main__":
    # Lista de interfaces (modifica esto para probar con tu interfaz específica)
    monitor_interface("\\Device\\NPF_{F0A73EDF-FF6E-4CE9-B594-03DA7816414B}")
   