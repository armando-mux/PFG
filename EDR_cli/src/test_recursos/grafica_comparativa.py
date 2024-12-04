import pandas as pd
import matplotlib.pyplot as plt

# Archivos CSV a comparar
archivo_1 = ".\\EDR_cli\\src\\test_recursos\\log1.csv"  # Reemplaza con el nombre del primer archivo
archivo_2 = ".\\EDR_cli\\src\\test_recursos\\log2.csv"  # Reemplaza con el nombre del segundo archivo

# Leer los archivos CSV en DataFrames
df1 = pd.read_csv(archivo_1)
df2 = pd.read_csv(archivo_2)

# Extraer las columnas numéricas (excepto Timestamp)
columnas_comparar = [col for col in df1.columns if col != "Timestamp"]

# Crear gráficos comparativos
for columna in columnas_comparar:
    plt.figure(figsize=(10, 6))
    plt.plot(df1.index, df1[columna], label=f"{archivo_1} - {columna}", marker='o')
    plt.plot(df2.index, df2[columna], label=f"{archivo_2} - {columna}", marker='x')
    plt.title(f"Comparativa de {columna}")
    plt.xlabel("Índice")
    plt.ylabel(columna)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
