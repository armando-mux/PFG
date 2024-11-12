import ctypes
import libpcap


def list_interfaces():
    # Creamos un puntero a la estructura pcap_if
    alldevs = ctypes.POINTER(libpcap.pcap_if_t)()
    errbuf = ctypes.create_string_buffer(256)

    # Llamamos a findalldevs con el puntero a pcap_if y el buffer de error
    result = libpcap.findalldevs(ctypes.byref(alldevs), errbuf)

    # Verificamos si ocurrió un error
    if result != 0:
        print("Error al obtener interfaces de red:", errbuf.value.decode())
        return

    # Iteramos sobre las interfaces utilizando el puntero
    iface = alldevs
    print("Interfaces de red disponibles:")
    contador = 1
    while iface:
        iface_name = iface.contents.name.decode()
        iface_desc = iface.contents.description.decode() if iface.contents.description else "Sin descripción"
        print(f"{contador} - Nombre: {iface_name}")
        print(f"Descripción: {iface_desc}")
        contador=contador+1

        # Pasar a la siguiente interfaz
        iface = iface.contents.next

    # Liberamos la memoria asignada por findalldevs
    libpcap.freealldevs(alldevs)

if __name__ == "__main__":
    list_interfaces()