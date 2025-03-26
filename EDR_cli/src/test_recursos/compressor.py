# comprimir_csv.py
import os
import zstandard as zstd

# Configuración
NIVEL_COMPRESION = 22  # Máxima compresión (rango 1-22)

def comprimir_csv(archivo):
    try:
        with open(archivo, 'rb') as f_in:
            with open(f"{archivo}.zst", 'wb') as f_out:
                zstd.ZstdCompressor(level=NIVEL_COMPRESION).copy_stream(f_in, f_out)
        os.remove(archivo)
        return True
    except Exception:
        return False

if __name__ == "__main__":
    csv_files = [f for f in os.listdir()]
    
    for csv in csv_files:
        if comprimir_csv(csv):
            print(f"Comprimido: {csv} → {csv}.zst")
        else:
            print(f"Error al comprimir: {csv}")