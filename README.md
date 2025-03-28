# PFG
En este repositorio se pueden encontrar los scripts desarrollados hasta el momento del PFG. En primer lugar, se resumen los datos recopilados en los scripts ya desarrollados, luego se enumeran las cosas que quedan por hacer en la etapa actual del proyecto (cosas implementables ya) y por último consideraciones sobre los sucesivos pasos a dar. 

## RESUMEN DEL ESTADO DEL PROYECTO

Dentro de /EDR_cli/src se encuentran los scripts que aportan las principales funcionalidades. Dentro de src, podemos encontrar  directorios. Todos ellos se subdividen en linux o windows que son las plataformas para las que había pensado desarrollar el programa. La razón por la que los he separado es que al final se empaquetará la aplicación en un .msi, un .deb o .rpm y de esta forma no es necesario duplicar archivos. Los datos que pretendo recolectar son los siguientes (algunos aún no estan implementados):

- Recursos de HW como memoria o CPU (falta implementar GPU).
- Procesos, servicios y cambios en los mismos.
- Actividad de red.
- Cambios en directorios y archivos clave.
- Registro de eventos clave como logueos, nuevos servicios o eventos de seguridad.
- Registro de syscall concretas (relacionadas con manipulacion de archivos o cifrado).

### HW_RESOURCES

En esta carpeta se encuenta el script que se encarga de registrar las estadísticas de uso de los recursos hardware principales. Para ello uso la libreria **psutil**, que salvo algunas diferencias usa funciones comunes para sistemas windows y basados en Unix. La información que recopila es la siguiente en caso de Windows:

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

El script toma una muestra de estos valores cada 1 segundos y lo registra en el archivo HW_resources_0.csv de la carpeta logs.

### Processes

En esta carpeta hay dos scripts para cada sistema operativo: en uno se registran los procesos y en otro los servicios.

#### Procesos 

En el caso de los procesos en ambos sistema operativos se usa la libreria **psutil**. En el caso de Windows los datos registrados son los siguientes:

| Campo                    |Descripción                                                                 |
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

En el caso del mismo script pero de Linux, los campos que constan son los siguientes:

| Campo                 | Descripción |
|-----------------------|-------------|
| **Timestamp**         | Fecha y hora exacta cuando se capturó la información del proceso. |
| **PID**               | Identificador único del proceso en el sistema. |
| **Nombre**            | Nombre del proceso o comando ejecutado. |
| **Ruta**              | Ubicación completa del ejecutable en el sistema de archivos. |
| **Usuario**           | Usuario propietario del proceso. |
| **Tiempo de creación** | Momento en que el proceso fue iniciado (tiempo desde el arranque del sistema o timestamp). |
| **Proceso padre**     | PID del proceso que creó este proceso. |
| **Numero lecturas**   | Cantidad total de operaciones de lectura realizadas por el proceso. |
| **Bytes leidos**      | Volumen total de datos leídos por el proceso. |
| **Numero escrituras** | Cantidad total de operaciones de escritura realizadas por el proceso. |
| **Bytes escritos**    | Volumen total de datos escritos por el proceso. |

#### Services
En el caso del listado de servicios, he escogido listar todos incluidos aquellos que estan en el equipo pero no activos. Para detectar los servicios de lo sitemas Windows, he usado de nuevo la libreria **psutil**. La lista de atributos de cada servicio es la siguiente:

| Campo                 | Descripción |
|-----------------------|-------------|
| **Timestamp**         | Fecha y hora exacta del escaneo. |
| **Nombre**            | Nombre del servicio. |
| **Estado**            | Estado actual del servicio (“running”, “paused”, “start_pending”, “pause_pending”, “continue_pending”, “stop_pending” o “stopped”). |
| **Auto-Start**        | Indica si el servicio se inicia automáticamente al arrancar el sistema (“automatic”, “manual” o “disabled”). |
| **PID**               | ID del proceso principal del servicio (vacío si no está activo). |
| **Ruta del ejecutable** | Ubicación completa del binario principal del servicio. |
| **Usuario**           | Usuario bajo el cual se ejecuta el servicio. |

En el caso de sistemas con SO basado en Linux he tenido que usar la utilidad en linea de comandos **systemctl** mediante la libreria **subprocess**, ya que la libreria psutil no da soporte a los servicios de este tipo de sistemas. La lista de campos que da por cada servicio detectado es la siguiente:

| Campo               | Descripción |
|---------------------|-------------|
| **timestamp**       | Fecha y hora del escaneo. |
| **service_name**    | Nombre completo del servicio. |
| **load_state**      | Estado de carga. |
| **active_state**    | Estado de ejecución. |
| **sub_state**       | Subestado detallado. |
| **description**     | Descripción del servicio. |
| **pid**             | ID del proceso principal (0 si no está activo). |
| **memory_usage**    | Consumo de memoria. |
| **cpu_percent**     | Uso de CPU |
| **file_path**       | Ruta completa del archivo de unidad de systemd (`.service`). |
| **time_start**      | Fecha/hora de inicio del servicio. |
| **time_end**        | Fecha/hora de finalización. |

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
|              | `C:\Windows\WinSxS\`                               |

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

### MAIN

En el main esta el script que lanza las funcionalidades ya mencionadas (menos la de test de recursos). Antes comprueba que esten las librerias usadas ya instaladas y, en caso de no estarlo, las instala (o lo intenta, estoy teniendo algunos problemas con Ubuntu y otros SO basados en Lnux). De todas formas esto es provisional, mi idea final es empaquetarlo todo como un programa instalable. 

-------------------------------------------------------



## COSAS QUE HACER 

- Eventos clave de windows + iaudit en Linux para monitorizar los mismos tipos de eventos.
- Syscalls en ambos equipos (al menos un conjunto relevante de syscalls)
- El script de directories es el que más CPU consume con diferencia: implementar buffer para hacer menos escrituras y, si no es suficiente, hacer filtros extra de qué eventos ignorar.
- Implementar lógica de los csv: ahora mismo crean archivos en /log y si ya estan creados, los continua. Implementar compresion automatica (zstd funciona bien) de los archivos para su envio a Azure cuando este hecha la parte de la nube.
- Process Monitor genera una imagen de todos los procesos activos cada 5 segundos y es el archivo de log más extenso con diferencia. En vez de una imagen de todos los procesos cada 5 segundos, puedo implementar una imagen completa inicial + registro de cada cambio significativo: destruccion de procesos, creacion de nuevos, cambios relevantes en campos de procesos preexistentes etc. Se puede hacer lo mismo con los servicios. 
- 

--------------------------------------------------------


## PRÓXIMOS PASOS

- Diseñar el uso de servicios de Azure Student (con este paquete me dan algunos servicios de la nube + 100$ para gastar en servicios extra).
- Usar alguna herramienta como [BeeWare](https://beeware.org/) para empaquetar el programa como .msi, .deb y .rpm
- He buscado repositorios de datos de comportamiento de equipos sin infectar o infectados, pero no he encontrado ninguno que contenga datos del equipo como tal. Es frecunte encontrar solamente escaneres de los procesos ejecutándose en el equipo o información solamente de la actividad de red. Por eso he pensado en generar datos de equipos sin infectar (reales y simulados con VM) y de equipos infectados con sandboxes (puede ser en local o usando herramientas de Azure).

## PREOCUPACIONES

- Algunos de los datos detectados redundan entre ellos: con eventos de windows puedes saber modificaciones a archivos clave que, en último término, es lo que esta haciendo el monitoreo de directorios por ejemplo. También puedes saber sobre creacion de nuevos procesos y sus característica, que es lo que hace el monitor de procesos. O con el analisis de llamadas al sistema puedes tener inforación también de lecturas y escrituras de archivos, que se solapa con el monitor de directorios.

- Me preocupa, de cada aspecto a monitorizar, estar cogiendo demasiados campos de información. Por una parte hace el programa de monitoreo más pesado. Por otra, genera más datos de cada sistema, lo que creo que hace que para poder establecer patrones válidos con los algoritmos de ML pertinentes se necesiten más equipos monitorizados. Dado que mi idea es generar yo esos datos, puede suponer un problema aún usando tecnicas de "data augmentation" o similar.
