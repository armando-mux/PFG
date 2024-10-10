import subprocess

# Define el comando de PowerShell para exportar los registros del Visor de Eventos
comando = """
$exportFilePath = "./event-log.txt"  # Ruta al archivo donde quieres exportar los registros
$logName = "Security"  # Nombre del registro que quieres exportar (por ejemplo, "System" o "Application")
$lastWeek = (Get-Date).AddDays(-1)  # Fecha de hace una semana

# Obtiene los eventos que ocurrieron en la última semana
$events = Get-WinEvent -LogName $logName | Where-Object { $_.TimeCreated -ge $lastWeek }

# Exporta los eventos a un archivo CSV
$events | Export-Csv -Path $exportFilePath -NoTypeInformation
"""

# Ejecuta el comando de PowerShell desde Python
subprocess.run(["powershell", "-Command", comando], check=True)

exit()