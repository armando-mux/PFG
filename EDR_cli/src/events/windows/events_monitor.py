import win32evtlog
import csv

# Configuración (misma que antes)
PATHS = ["Security", "System", "Application"]
EVENTOS_A_MONITOREAR = {4663, 4688, 1102}
CSV_FILE = "eventos_ransomware.csv"

def pepito_grillo(reason, context, evt):
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
    Callback=pepito_grillo,
    Query="*[System[(EventID=4624 or EventID=4625 or EventID=4688 or EventID=6005 or EventID=6006 or EventID=7036 or EventID=1000)]]"
)
print("Suscripción a eventos de seguridad creada.")

h_suscription2 = win32evtlog.EvtSubscribe(
    ChannelPath="System",
    Flags=win32evtlog.EvtSubscribeToFutureEvents,
    Callback=pepito_grillo,
    Query="*[System[(EventID=4624 or EventID=4625 or EventID=4688 or EventID=6005 or EventID=6006 or EventID=7036 or EventID=1000)]]"
)
print("Suscripción a eventos del sistema creada.")

h_suscription3 = win32evtlog.EvtSubscribe(
    ChannelPath="Application",
    Flags=win32evtlog.EvtSubscribeToFutureEvents,
    Callback=pepito_grillo,
    Query="*[System[(EventID=4624 or EventID=4625 or EventID=4688 or EventID=6005 or EventID=6006 or EventID=7036 or EventID=1000)]]"
)
print("Suscripción a eventos de aplicación creada.")

# Mantener el script activo
import time
try:
    while True:
        time.sleep(0.1)  # Reducido a mínimo consumo
except KeyboardInterrupt:
    pass