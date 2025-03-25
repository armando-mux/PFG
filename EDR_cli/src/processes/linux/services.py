import subprocess
import csv
from datetime import datetime
import time

# Configuración
csv_file = "services_monitor.csv"

# Cabeceras del CSV
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
]

def get_systemctl_services():
    """Obtiene la lista de servicios con systemctl y devuelve datos estructurados."""
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
        for line in output[1:-7]:  # Ignora encabezados y líneas vacías
            if line.strip():
                parts = line.split()
                service_name = parts[0]
                
                # Obtiene detalles adicionales con systemctl show
                show_cmd = ["systemctl", "show", "*.service", "--property=LoadState,ActiveState,SubState,Description,MainPID,MemoryCurrent,CPUUsage,Names"]
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

def write_to_csv(data):
    """Escribe los datos en el archivo CSV."""
    file_exists = False
    try:
        with open(csv_file, "r") as f:
            file_exists = True
    except FileNotFoundError:
        pass
    
    with open(csv_file, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        if not file_exists:
            writer.writeheader()
        
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
