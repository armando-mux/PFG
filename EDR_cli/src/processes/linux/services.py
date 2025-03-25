import subprocess
import csv
from datetime import datetime
import time
from pathlib import Path  

# Configuración del archivo CSV
ruta_log = Path(__file__).resolve().parent.parent.parent.parent / "logs" 
csv_file = f"{ruta_log}/services_monitor.csv"

headers = [
    "timestamp",
    "service_name",
    "load_state",
    "active_state",
    "sub_state",
    "description",
    "pid",
    "memory_usage",
    "cpu_percent"
    "file_path",
    "time_start",
    "time_end"
]

# Obtiene la información de los servicios con systemctl y la devuelve en una lista de diccionarios.
def get_systemctl_services():

    try:
        # Ejecuta systemctl y captura la salida
        cmd = [
            "systemctl",
            "list-units",
            "--type=service",
            "--all",
            "--no-pager",
            "--plain"
        ]
        output = subprocess.check_output(cmd, text=True).splitlines()
        
        services = []
        for line in output[1:-7]:  
            if line.strip():
                parts = line.split()
                service_name = parts[0]
                
                # Obtiene detalles adicionales con systemctl show
                show_cmd = ["systemctl", "show", "*.service", "--property=LoadState,ActiveState,SubState,Description,MainPID,MemoryCurrent,CPUUsage,FragmentPath,ExecMainStartTimestamp,ExecMainExitTimestamp"]
                show_output = subprocess.check_output(show_cmd, text=True)
                
                # Parsea la salida
                service_data = {"service_name": service_name}
                for prop in show_output.splitlines():
                    if "=" in prop:
                        key, value = prop.split("=", 1)
                        service_data[key.lower()] = value if value else "not-found"
                
                services.append(service_data)
        
        return services
    
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar systemctl: {e}")
        return []

# Escribe la información de los servicios en el archivo CSV.
def write_to_csv(data):
    
    with open(csv_file, "a", newline="", encoding="utf-8") as f:
        if f.tell() == 0:
            writer = csv.DictWriter(f, fieldnames=headers)
        
        for service in data:
            row = {
                "timestamp": datetime.now().isoformat(),
                "service_name": service.get("service_name", "N/A"),
                "load_state": service.get("loadstate", "not-found"),
                "active_state": service.get("activestate", "not-found"),
                "sub_state": service.get("substate", "not-found"),
                "description": service.get("description", "N/A"),
                "pid": service.get("mainpid", "not-found"),
                "memory_usage": int(service.get('memorycurrent', 0)) if service.get("memorycurrent") not in ["", "not-found", "[not set]"] else "not set",
                "cpu_percent": float(service.get('cpuusage', 0)) if service.get("cpuusage") not in ["", "[not set]"] else "not set"
                "file_path": service.get("fragmentpath", "not-found"),
                "time_start": service.get("execmainstarttimestamp", "not-found"),
                "time_end": service.get("execmainexittimestamp", "not-found")
            }
            writer.writerow(row)

def main():
    print(f"Monitorizando servicios con systemctl. Guardando en {csv_file}")
    try:
        while True:
            services = get_systemctl_services()
            if services:
                write_to_csv(services)
                print(f"[{datetime.now().isoformat()}] Registrados {len(services)} servicios.")
            time.sleep(1800)
    except KeyboardInterrupt:
        print("\nMonitorización detenida.")

if __name__ == "__main__":
    main()
