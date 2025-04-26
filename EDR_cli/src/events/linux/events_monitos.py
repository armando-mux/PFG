from pathlib import Path
import re
import subprocess
import csv

ruta_log = Path(__file__).resolve().parent.parent.parent.parent / "logs" / "events.csv"
campos = ["timestamp", "event_id", "type", "uid", "auid", "exe", "syscall", "success", "path", "key", "host"]
expresion_regular = re.compile(r'type=([A-Z_]+)\s+msg=audit\((\d+)\.(\d+):(\d+)\):\s(.*)')
    
# Definimos las reglas que queremos aplicar
reglas = [
    # --- Usuarios y privilegios ---
    ["auditctl", "-w", "/etc/passwd", "-p", "wa", "-k", "passwd_changes"],
    ["auditctl", "-w", "/etc/group", "-p", "wa", "-k", "group_changes"],
    ["auditctl", "-w", "/etc/shadow", "-p", "wa", "-k", "shadow_changes"],
    ["auditctl", "-w", "/etc/sudoers", "-p", "wa", "-k", "sudoers_changes"],

    # --- Actividad de su y sudo ---
    ["auditctl", "-a", "always,exit", "-F", "path=/usr/bin/su", "-F", "perm=x", "-k", "su_attempt"],
    ["auditctl", "-a", "always,exit", "-F", "path=/usr/bin/sudo", "-F", "perm=x", "-k", "sudo_exec"],

    # --- Tareas programadas ---
    ["auditctl", "-w", "/etc/cron.d/", "-p", "wa", "-k", "cron_changes"],
    ["auditctl", "-w", "/etc/cron.daily/", "-p", "wa", "-k", "cron_daily_changes"],
    ["auditctl", "-w", "/var/spool/cron/", "-p", "wa", "-k", "spool_cron_changes"],

    # --- Cambios de servicios ---
    ["auditctl", "-w", "/etc/systemd/system/", "-p", "wa", "-k", "systemd_services_changes"],

    # --- Acceso a claves SSH ---
    ["auditctl", "-w", "/home/", "-p", "wa", "-k", "ssh_keys_changes"],

    # --- Logs importantes ---
    ["auditctl", "-w", "/var/log/auth.log", "-p", "wa", "-k", "authlog_changes"],
    ["auditctl", "-w", "/var/log/syslog", "-p", "wa", "-k", "syslog_changes"],
    ["auditctl", "-w", "/var/log/audit/", "-p", "wa", "-k", "auditlog_changes"],

    # --- Firewall configuraciones ---
    ["auditctl", "-w", "/etc/iptables/", "-p", "wa", "-k", "iptables_changes"],
    ["auditctl", "-w", "/etc/ufw/", "-p", "wa", "-k", "ufw_changes"],

    # --- Hostname y configuración de red ---
    ["auditctl", "-w", "/etc/hostname", "-p", "wa", "-k", "hostname_changes"],
    ["auditctl", "-w", "/etc/hosts", "-p", "wa", "-k", "hostsfile_changes"],
    ["auditctl", "-w", "/etc/resolv.conf", "-p", "wa", "-k", "resolv_changes"],

    # --- Ejecución de scripts en /tmp ---
    ["auditctl", "-a", "always,exit", "-F", "dir=/tmp/", "-F", "perm=x", "-k", "tmp_script_exec"]
]


def aplicar_reglas():
    print("[*] Aplicando reglas de monitoreo de inicio de sesión...")
    for regla in reglas:
        try:
            subprocess.run(regla, check=True)
            print(f"[+] Regla aplicada: {' '.join(regla)}")
        except subprocess.CalledProcessError as e:
            print(f"[!] Error aplicando regla: {' '.join(regla)}")
            print(f"    {e}")
            
def extraer_campos(tipo, timestamp, id, data):
    campos = {
        "timestamp": timestamp,
        "event_id": id,
        "type": tipo,
        "uid": "N/A",
        "auid": "N/A",
        "exe": "N/A",
        "syscall": "N/A",
        "success": "N/A",
        "path": "N/A",
        "key": "N/A",
        "host": "N/A"
    }
    for k in ["uid", "auid", "exe", "syscall", "success", "key", "path", "host"]:
        match = re.search(rf"{k}=([^\s]+)", data)
        if match:
            campos[k] = match.group(1)  
            
    return campos
    
                
def main():
    aplicar_reglas()
    
    comando = subprocess.Popen(
        ["tail", "-F", "/var/log/audit/audit.log"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )   
    
    with open(ruta_log, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=campos)
        writer.writeheader()
        if file.tell() == 0:
            writer.writeheader()
        for line in comando.stdout:
            match = expresion_regular.search(line)
            if match:
                tipo, ts_sec, ts_usec, id, datos = match.groups()
                timestamp = f"{ts_sec}.{ts_usec}"
                row = extraer_campos(tipo, timestamp, id, datos)
                writer.writerow(row)
                print(f"[+] Evento registrado: {row['type']} {row['timestamp']} key={row['key']}")
                
if __name__ == "__main__":
    main()
    
