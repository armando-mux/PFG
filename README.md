# PFG
En este repositorio se pueden encontrar los scripts desarrollados hasta el momento del PFG. 

## RESUMEN DEL ESTADO DEL PROYECTO

Dentro de /EDR_cli/src se encuentran los scripts que aportan las principales funcionalidades. Dentro de src, podemos encontrar 4 directorios. Todos ellos se subdividen en linux o windows que son las plataformas para las que había pensado desarrollar el programa. 

### HW_RESOURCES

En esta carpeta se encuenta el script que se encarga de registrar las estadísticas de uso de los recursos hardware principales. Para ello uso la libreria **psutil**, que salvo algunas diferencias usa funciones comunes para sistemas windows y basados en unix. La información que recopila es la siguiente en caso de Windows:

| Campo | Significado |
|-------------|-------|
| **Timestamp** | Fecha y hora en que se registraron los datos. |
| **CPU Total (%)** | Porcentaje total de uso de la CPU. |
| **CPU User (%)** | Porcentaje de uso de la CPU por procesos de usuario. |
| **CPU System (%)** | Porcentaje de uso de la CPU por procesos del sistema. |
| **CPU Idle (%)** | Porcentaje de tiempo que la CPU está inactiva. |
| **CPU Interrupt (%)** | Porcentaje de tiempo que la CPU está manejando interrupciones. |
| **CPU DCP (%)** | Porcentaje de tiempo que la CPU está en modo de bajo consumo (DCP). |
| **Mem Total** | Memoria RAM total disponible en el sistema. |
| **Mem Available** | Memoria RAM disponible para su uso. |
| **Mem Percent** | Porcentaje de memoria RAM utilizada. |
| **Mem Used** | Cantidad de memoria RAM utilizada. |
| **Mem Free** | Cantidad de memoria RAM libre. |
| **Swap Total** | Cantidad total de espacio de intercambio (swap). |
| **Swap Used** | Cantidad de espacio de intercambio utilizado. |
| **Swap Free** | Cantidad de espacio de intercambio libre. |
| **Swap Percent** | Porcentaje de espacio de intercambio utilizado. |
| **Swap Sin** | Cantidad de datos leídos desde el disco al espacio de intercambio. |
| **Swap Sout** | Cantidad de datos escritos desde el espacio de intercambio al disco. |
| **Disco - Lecturas Completadas** | Número de lecturas completadas en el disco. |
| **Disco - Escrituras Completadas** | Número de escrituras completadas en el disco. |

En el caso del script para Linux, varían algunos de los campos por diferencias en la libreria y en la gestion de memoria de los dos SO:

| Campo | Significado |
|-------------|-------|
| **Timestamp** | Fecha y hora en que se registraron los datos. |
| **CPU Total** | Uso total de la CPU. |
| **CPU User** | Uso de la CPU por procesos de usuario. |
| **CPU Nice** | Uso de la CPU por procesos con prioridad "nice" (baja prioridad). |
| **CPU System** | Uso de la CPU por procesos del sistema. |
| **CPU Idle** | Tiempo que la CPU está inactiva. |
| **CPU Iowait** | Tiempo que la CPU espera por operaciones de E/S. |
| **CPU Irq** | Tiempo que la CPU maneja interrupciones de hardware (IRQ). |
| **CPU SoftIrq** | Tiempo que la CPU maneja interrupciones de software (SoftIRQ). |
| **CPU Steal** | Tiempo que la CPU espera debido a la virtualización (steal time). |
| **CPU Guest** | Tiempo que la CPU ejecuta un sistema operativo invitado (guest). |
| **CPU Guest Nice** | Tiempo que la CPU ejecuta un sistema operativo invitado con prioridad "nice". |
| **Mem Total** | Memoria RAM total disponible en el sistema. |
| **Mem Available** | Memoria RAM disponible para su uso. |
| **Mem Percent** | Porcentaje de memoria RAM utilizada. |
| **Mem Used** | Cantidad de memoria RAM utilizada. |
| **Mem Free** | Cantidad de memoria RAM libre. |
| **Mem Active** | Memoria RAM activa en uso. |
| **Mem Inactive** | Memoria RAM inactiva (no en uso activo). |
| **Buffers** | Memoria utilizada como búfer para operaciones de E/S. |
| **Cached** | Memoria utilizada como caché para acelerar accesos. |
| **Shared** | Memoria compartida entre procesos. |
| **Slab** | Memoria utilizada por el kernel para estructuras de datos. |
| **Swap Total** | Cantidad total de espacio de intercambio (swap). |
| **Swap Used** | Cantidad de espacio de intercambio utilizado. |
| **Swap Free** | Cantidad de espacio de intercambio libre. |
| **Swap Percent** | Porcentaje de espacio de intercambio utilizado. |
| **Swap Sin** | Cantidad de datos leídos desde el disco al espacio de intercambio. |
| **Swap Sout** | Cantidad de datos escritos desde el espacio de intercambio al disco. |
| **Disco - Lecturas Completadas** | Número de lecturas completadas en el disco. |
| **Disco - Escrituras Completadas** | Número de escrituras completadas en el disco. |

El script toma una muestra de estos valores cada 1 segundos y lo registra en el archivo HW_resources_0.csv de la carpeta logs. La muestra que se encuentra ahora mismo corresponde a una ejecucion en  Windows.

### processes

En esta carpeta hay dos scripts para cada sistema operativo: en uno se registran los procesos y en otro los servicios.

#### Procesos 

En el caso de los procesos en ambos sistema operativos se usa la libreria **psutil**. En el caso de Windows los datos registrados son los siguientes:

| Campo                      | Descripción                                                                 |
|----------------------------|-----------------------------------------------------------------------------|
| **Timestamp**              | Fecha y hora exacta de la captura de datos.              |
| **PID**                    | Identificador numérico único del proceso en el sistema.                     |
| **Nombre**                 | Nombre del archivo ejecutable del proceso.                |
| **Ruta**                   | Ubicación completa en disco del ejecutable del proceso.                     |
| **Usuario**                | Usuario que ejecuta el proceso.       |
| **Tiempo de creación**     | Fecha y hora cuando se inició el proceso.                                   |
| **Proceso padre**          | PID del proceso que creó este proceso.                                      |
| **Número lecturas**        | Cantidad total de operaciones de lectura realizadas por el proceso.         |
| **Bytes leídos**           | Volumen total de datos leídos (en bytes).                                   |
| **Número escrituras**      | Cantidad total de operaciones de escritura realizadas.                      |
| **Bytes escritos**         | Volumen total de datos escritos (en bytes).                                 |
| **Número otras operaciones** | Operaciones de E/S que no son lectura/escritura (ej: control/llamadas).   |
| **Bytes otras operaciones** | Datos transferidos en operaciones no estándar (bytes).                     |



### NETWORK

En la carpeta network, encontramos los scripts network.py en las carpetas Linux y Windows. En este caso, la información que se recopila es identica pero la forma de listar las interfaces de red a monitorizar es distinta. Se usa el paquete **pyshark** en este caso. La información que se recoge en el csv es la siguiente:

| Campo | Significado |
|-------------|-------|
| **timestamp** | Fecha y hora en que se capturó el paquete. |
| **ip_src** | Dirección IP de origen del paquete. |
| **ip_dst** | Dirección IP de destino del paquete. |
| **port_src** | Puerto de origen del paquete. |
| **port_dst** | Puerto de destino del paquete. |
| **transport_protocol** | Protocolo de transporte utilizado. |
| **app_protocol** | Protocolo de aplicación detectado. |
| **length** | Longitud total del paquete en bytes. |

En el caso de paquetes de protocolos como ARP o ICMP, los valores de port_src, port_dst y de transport_protocol será N/A.

### DIRECTORIES

En este caso, en ambos scripts (para Linux y Windows) uso la libreria **watchdog** para vigilar y registrar los cambios, creaciones o borrados de directorios y archivos en localizaciones clave del sistema operativo. Los directorios a monitorear serán los siguientes:

| Linux       | Windows                                              |
|-------------|------------------------------------------------------|
| `/home/`    | `C:\Users`                                           |
| `/usr/bin/` | `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\` |
| `/tmp/`     | `C:\Windows\Temp\`                                   |
| `/var/tmp/` | `C:\Windows\Tasks\`                                  |
| `/mnt/`     | `C:\Windows\System32\`                               |
|             | `C:\Windows\SysWOW64\`                               |

La información mostrada de cada evento es la siguiente: 

| Campo        | Descripción                                                                 |
|--------------|-----------------------------------------------------------------------------|
| **Date**     | Fecha en la que ocurrió el evento.                    |
| **Time**     | Hora en la que ocurrió el evento.                       |
| **Event**    | Tipo de evento registrado (creación, modificación, eliminación).             |
| **Path src** | Ruta de origen del archivo o directorio involucrado en el evento.            |
| **Path Dst** | Ruta de destino del archivo o directorio                                    |
| **Archive**  | Nombre del archivo involucrado en el evento                                    |
| **isDirectory** | Indica si es un directorio. En caso contrario es un archivo              |

En ambos casos he tenido que incorporar listas de exclusión de directorios porque a veces se crean bucles infinitos. 

### TEST_RECURSOS

Esta carpeta no tiene demasiado interés. Estaba preocupado por el consumo de recursos de los scripts siendo ejecutados simultaneamente, y esto es para medir el uso de recursos del sistema sin ejecutarlos y ejecutándolos, y luego compararlos. No indica un aumento de uso de recursos significativo (ni en los numeros ni en las gráficas), pero ni es un script muy fino ni estan finalizadas todas las funcionalidades. 

### MAIN

En el main esta el script que lanza las funcionalidades ya mencionadas (menos la de test de recursos). Antes comprueba que esten las librerias usadas ya instaladas y, en caso de no estarlo, las instala (o lo intenta, he tenido algunos problemas con Ubuntu). De todas formas esto es provisional, mi idea final la comento en la siguiente sección. 

-------------------------------------------------------

to-do antes de enviar: 

- Eventos clave de windows 
- Script de iaudit en linux
- Syscalls en ambos equipos
- Ajustar numero de escrituras en directories windows para bajar cpu¿?
- Revisar datos de hw y ver GPU.
- Implementar logica de los csv: como minimo no eliminarlos y si creamos sistema de rotacion de archivos mejor que mejor.
- process monitor cada 5 segundos genera lista completa y es el archivo más pesado. Hacer por eventos?