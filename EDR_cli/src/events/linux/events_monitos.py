import subprocess

# Definimos las reglas que queremos aplicar
reglas = [
    ["auditctl", "-w", "/usr/bin/login", "-p", "x", "-k", "login_monitor"],
    ["auditctl", "-w", "/usr/sbin/sshd", "-p", "x", "-k", "ssh_monitor"],
    ["auditctl", "-w", "/usr/bin/su", "-p", "x", "-k", "su_monitor"],
    ["auditctl", "-w", "/usr/bin/sudo", "-p", "x", "-k", "sudo_monitor"]
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
