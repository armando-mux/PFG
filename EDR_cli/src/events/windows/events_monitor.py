import os
from pathlib import Path
import socket
import sys
import win32evtlog
import csv
import time
import datetime
import xml.etree.ElementTree as ET

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
from src import utils



def callback(reason, context, evt):
    writer, file = context
    try:
        # Verifica si el evento es válido
        if not evt:
            print("Evento inválido: evt es None")
            return 0
            
        # Método más robusto para obtener el EventID
        xml = ET.fromstring(win32evtlog.EvtRender(evt, win32evtlog.EvtRenderEventXml))
        provider = xml.find('.//{*}Provider').attrib
        eventid = xml.find('.//{*}EventID').text
        level = xml.find('.//{*}Level').text
        channel = xml.find('.//{*}Channel').text
        
        time = xml.find('.//{*}TimeCreated').attrib
        time = time['SystemTime']
        if '.' in time:
            main_part, fraction = time.split('.')
            fraction = fraction.rstrip('Z')  
            fraction = (fraction + '000000')[:6]  
            time = f"{main_part}.{fraction}Z"
        time = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
        time = time.replace(tzinfo=datetime.timezone.utc).astimezone()
        computer = xml.find('.//{*}Computer').text
        
        
       
        # Escribir la fila en el CSV
        writer.writerow({
            'Provider': provider['Name'],
            'EventID': eventid,
            'Level': level,
            'Channel': channel,
            'TimeCreated': time,
            'Computer': computer
        })
        file.flush()
        
    except Exception as e:
        print(f"Error en callback: {str(e)}")
    return 0

def register_events(csv_file, max_file_size):
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        fieldnames = ['Provider', 'EventID', 'Level', 'Channel', 'TimeCreated', 'Computer']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0:
            writer.writeheader()
        context = (writer, file)

        # Suscripción en tiempo real
        h_subscription1 = win32evtlog.EvtSubscribe(
            ChannelPath="Security",
            Flags=win32evtlog.EvtSubscribeToFutureEvents,
            Callback=callback,
            Context=context,
            Query="*[System[(EventID=4663 or EventID=4656 or EventID=4719 or EventID=4688 or EventID=4624 or EventID=4625 or EventID=4673 or EventID=4672 or EventID=1102 or EventID=5058 or EventID=5061 or EventID=5157 or EventID=4698 or EventID=4702 or EventID=4689 or EventID=5156 or EventID=5158 or EventID=5025 or EventID=5031 or EventID=4720 or EventID=4738 or EventID=4742)]]"
        )
        print("Suscripción a eventos de seguridad creada.")

        h_suscription2 = win32evtlog.EvtSubscribe(
            ChannelPath="System",
            Flags=win32evtlog.EvtSubscribeToFutureEvents,
            Callback=callback,
            Context=context,
            Query="*[System[(EventID=7036 or EventID=104 or EventID=7034 or EventID=7045 or EventID=753 or EventID=7040 or EventID=1042 or EventID=13 or EventID=10016 or EventID=1074 or EventID=6005 or EventID=6006 or EventID=6011 or EventID=7022 or EventID=7023 or EventID=7024 or EventID=106 or EventID=140 or EventID=11 or EventID=98 or EventID=99)]]"
        )
        print("Suscripción a eventos del sistema creada.")

        h_suscription3 = win32evtlog.EvtSubscribe(
            ChannelPath="Application",
            Flags=win32evtlog.EvtSubscribeToFutureEvents,
            Callback=callback,
            Context=context,
            Query="*[System[(EventID=1016 or EventID=1017 or EventID=1000 or EventID=1009 or EventID=1116)]]"
        )
        print("Suscripción a eventos de aplicación creada.")

        h_suscription4 = win32evtlog.EvtSubscribe(
            ChannelPath="Microsoft-Windows-WMI-Activity/Operational",
            Flags=win32evtlog.EvtSubscribeToFutureEvents,
            Callback=callback,
            Context=context,
            Query="*[System[(EventID=10000 or EventID=10001)]]"
        )
        print("Suscripción a eventos de WMI creada.")

        h_suscription5 = win32evtlog.EvtSubscribe(
            ChannelPath="Microsoft-Windows-PowerShell/Operational",
            Flags=win32evtlog.EvtSubscribeToFutureEvents,
            Callback=callback,
            Context=context,
            Query="*[System[(EventID=4103 or EventID=4104)]]"
        )
        print("Suscripción a eventos de PowerShell creada.")

        h_suscription6 = win32evtlog.EvtSubscribe(
            ChannelPath="Microsoft-Windows-PrintService/Operational",
            Flags=win32evtlog.EvtSubscribeToFutureEvents,
            Callback=callback,
            Context=context,
            Query="*[System[(EventID=90 or EventID=92)]]"
        )
        print("Suscripción a eventos de PrintService creada.")

        h_suscription7 = win32evtlog.EvtSubscribe(
            ChannelPath="Microsoft-Windows-GroupPolicy/Operational",
            Flags=win32evtlog.EvtSubscribeToFutureEvents,
            Callback=callback,
            Context=context,
            Query="*[System[(EventID=1024 or EventID=24577 or EventID=24576 or EventID=106 or EventID=104)]]"
        )
        print("Suscripción a eventos de GroupPolicy creada.")

        try: 
            while not (os.path.exists(csv_file) and os.path.getsize(csv_file) > max_file_size):
                time.sleep(0.1)  # Reducido a mínimo consumo
        finally:        
            h_subscription1.close()
            h_suscription2.close()
            h_suscription3.close()
            h_suscription4.close()
            h_suscription5.close()
            h_suscription6.close()
            h_suscription7.close()
     

def main(): 
    file_counter = 0
    max_file_size = 100 * 1024  # 1 MB 
    ruta_log = Path(__file__).resolve().parent.parent.parent.parent / "logs"
    name_base =  f"events{file_counter}.csv"
    csv_file = f"{ruta_log}/{name_base}"
    try:
        while True:
            register_events(csv_file=csv_file, max_file_size=max_file_size)
            name = socket.gethostname()
            nombre_1 = f"{name}/EVENTS/{name_base}"
            utils.send_file(csv_file, "prueba", nombre_1)
            os.remove(csv_file)
            file_counter += 1
            name_base = f"events{file_counter}.csv"
            csv_file = f"{ruta_log}/{name_base}"
            
    except KeyboardInterrupt:
        print("Monitoreo detenido por el usuario.")
        name = socket.gethostname()
        nombre_1 = f"{name}/EVENTS/{name_base}"
        utils.send_file(csv_file, "prueba", nombre_1)
        os.remove(csv_file)
    
    
# Mantener el script activo
if __name__ == "__main__":
    main()
    