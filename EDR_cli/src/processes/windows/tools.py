import pandas as pd

def cargar_csv_a_dataframe(csv_file):
    """Carga un archivo CSV en un DataFrame de Pandas."""
    try:
        # Cargar el CSV en un DataFrame
        df = pd.read_csv(csv_file)
        print("CSV cargado exitosamente en un DataFrame.")
        return df
    except Exception as e:
        print(f"Error al cargar el CSV: {e}")
        return None

def mostrar_info_dataframe(df):
    """Muestra información básica del DataFrame."""
    if df is not None:
        print("\n--- Información del DataFrame ---")
        print(f"Número de filas y columnas: {df.shape}")
        print("\nPrimeras 5 filas:")
        print(df.head())
        print("\nResumen estadístico:")
        print(df.describe())
        print("\nInformación general:")
        print(df.info())

def verificar_duplicados(df):
    """Verifica si hay filas duplicadas en el DataFrame."""
    if df is not None:
        duplicados = df[df.duplicated()]
        if not duplicados.empty:
            print("\n--- Filas duplicadas encontradas ---")
            print(duplicados)
        else:
            print("\nNo se encontraron filas duplicadas en el DataFrame.")
            
        duplicadosPID = df[df.duplicated(subset=["PID"])]
        if not duplicadosPID.empty:
            print("\n--- PID duplicados encontrados ---")
            print(duplicadosPID)
        else:
            print("\nNo se encontraron PID duplicados en el DataFrame.")
if __name__ == "__main__":
    csv_file = "C:\\Users\\arman\\Documents\\UNED\\PFG\\Pydev\\PFG\\EDR_cli\\logs\\process_monitor.csv"  # Cambia esto por la ruta de tu archivo CSV
    df = cargar_csv_a_dataframe(csv_file)
    mostrar_info_dataframe(df)
    verificar_duplicados(df)
