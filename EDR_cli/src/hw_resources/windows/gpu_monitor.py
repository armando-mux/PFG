import csv
import os
import subprocess
import time
from datetime import datetime

def is_nvidia_gpu_available():
    """Check if NVIDIA GPU is available using nvidia-smi."""
    try:
        result = subprocess.run(["nvidia-smi"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def parse_nvidia_smi_output():
    """Parse GPU usage stats using nvidia-smi query."""
    query_fields = [
        "timestamp", "utilization.gpu", "memory.used", "memory.total", "temperature.gpu", "name"
    ]
    command = [
        "nvidia-smi",
        f'--query-gpu={",".join(query_fields)}',
        "--format=csv,noheader,nounits"
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError("Failed to run nvidia-smi query.")
    lines = result.stdout.strip().split('\n')
    parsed_data = []
    for line in lines:
        parts = [p.strip() for p in line.split(',')]
        parsed_data.append(parts)
    return parsed_data

def write_to_csv(csv_file_path, headers, data_rows):
    """Write data to CSV file, appending new rows."""
    file_exists = os.path.isfile(csv_file_path)
    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(headers)
        for row in data_rows:
            writer.writerow(row)

# Only run the monitor if a NVIDIA GPU is available
if is_nvidia_gpu_available():
    csv_path = "gpu.csv"
    headers = ["timestamp", "gpu_name", "gpu_utilization_percent", "memory_used_MB", "memory_total_MB", "temperature_C"]
    
    print("NVIDIA GPU detected. Starting monitoring...")
    print("Logging data to:", csv_path)
    
    try:
        for _ in range(5):  # Limited to 5 iterations for testing; replace with `while True:` in production
            gpu_stats = parse_nvidia_smi_output()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            formatted_rows = [
                [timestamp, gpu_name, util, mem_used, mem_total, temp]
                for gpu_name, util, mem_used, mem_total, temp, _ in gpu_stats
            ]
            write_to_csv(csv_path, headers, formatted_rows)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
    except Exception as e:
        print("Error during monitoring:", e)
else:
    print("No NVIDIA GPU found. Exiting script.")
