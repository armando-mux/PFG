import subprocess

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

def listar_reglas():
    print("\n[*] Reglas activas actualmente:")
    subprocess.run(["auditctl", "-l"])

if __name__ == "__main__":
    if subprocess.geteuid() != 0:
        print("[!] Debes ejecutar este script como root.")
    else:
        aplicar_reglas()
        listar_reglas()
