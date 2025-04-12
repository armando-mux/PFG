import win32evtlog
import csv

# Configuración (misma que antes)

EVENTOS_A_MONITOREAR = {4663, 4688, 1102}
CSV_FILE = "eventos_ransomware.csv"

def callback(reason, context, evt):
    try:
        # Verifica si el evento es válido
        if not evt:
            print("Evento inválido: evt es None")
            return 0
            
        # Método más robusto para obtener el EventID
        xml = win32evtlog.EvtRender(evt, win32evtlog.EvtRenderEventXml)
        print(f"Evento XML: {xml}")  
    except Exception as e:
        print(f"Error en callback: {str(e)}")
    return 0

# Suscripción en tiempo real
h_subscription = win32evtlog.EvtSubscribe(
    ChannelPath="Security",
    Flags=win32evtlog.EvtSubscribeToFutureEvents,
    Callback=callback,
    Query="*[System[(EventID=4663 or EventID=4656 or EventID=4719 or EventID=4688 or EventID=4624 or EventID=4625 or EventID=4673 or EventID=4672 or EventID=1102 or EventID=5058 or EventID=5061 or EventID=5157 or EventID=4698 or EventID=4702 or EventID=4689 or EventID=5156 or EventID=5158 or EventID=5025 or EventID=5031 or EventID=4720 or EventID=4738 or EventID=4742)]]"
)
print("Suscripción a eventos de seguridad creada.")

h_suscription2 = win32evtlog.EvtSubscribe(
    ChannelPath="System",
    Flags=win32evtlog.EvtSubscribeToFutureEvents,
    Callback=callback,
    Query="*[System[(EventID=7036 or EventID=104 or EventID=7034 or EventID=7045 or EventID=753 or EventID=7040 or EventID=1042 or EventID=13 or EventID=10016 or EventID=1074 or EventID=6005 or EventID=6006 or EventID=6011 or EventID=7022 or EventID=7023 or EventID=7024 or EventID=106 or EventID=140 or EventID=11 or EventID=98 or EventID=99)]]"
)
print("Suscripción a eventos del sistema creada.")

h_suscription3 = win32evtlog.EvtSubscribe(
    ChannelPath="Application",
    Flags=win32evtlog.EvtSubscribeToFutureEvents,
    Callback=callback,
    Query="*[System[(EventID=1016 or EventID=1017 or EventID=1000 or EventID=1009 or EventID=1116)]]"
)
print("Suscripción a eventos de aplicación creada.")

h_suscription4 = win32evtlog.EvtSubscribe(
    ChannelPath="Microsoft-Windows-WMI-Activity/Operational",
    Flags=win32evtlog.EvtSubscribeToFutureEvents,
    Callback=callback,
    Query="*[System[(EventID=10000 or EventID=10001)]]"
)
print("Suscripción a eventos de WMI creada.")

h_suscription5 = win32evtlog.EvtSubscribe(
    ChannelPath="Microsoft-Windows-PowerShell/Operational",
    Flags=win32evtlog.EvtSubscribeToFutureEvents,
    Callback=callback,
    Query="*[System[(EventID=4103 or EventID=4104)]]"
)
print("Suscripción a eventos de PowerShell creada.")

h_suscription6 = win32evtlog.EvtSubscribe(
    ChannelPath="Microsoft-Windows-PrintService/Operational",
    Flags=win32evtlog.EvtSubscribeToFutureEvents,
    Callback=callback,
    Query="*[System[(EventID=90 or EventID=92)]]"
)
print("Suscripción a eventos de PrintService creada.")

h_suscription7 = win32evtlog.EvtSubscribe(
    ChannelPath="Microsoft-Windows-GroupPolicy/Operational",
    Flags=win32evtlog.EvtSubscribeToFutureEvents,
    Callback=callback,
    Query="*[System[(EventID=1024 or EventID=24577 or EventID=24576 or EventID=106 or EventID=104)]]"
)
print("Suscripción a eventos de GroupPolicy creada.")


# Mantener el script activo
import time
try:
    while True:
        time.sleep(0.1)  # Reducido a mínimo consumo
except KeyboardInterrupt:
    pass