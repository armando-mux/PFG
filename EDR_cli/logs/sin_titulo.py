import pandas as pd

pd.options.display.max_columns = None

# Cargar el archivo CSV en un DataFrame
df = pd.read_csv('C:\\Users\\arman\\Documents\\UNED\\PFG\\Pydev\\PFG\\EDR_cli\\logs\\filesystem_event.csv', sep=',', encoding='utf-8')

# Verificar los primeros registros para saber cómo está estructurado el archivo
print(df.head())
print(df.columns)



# Contar los valores únicos en el campo especificado


# Mostrar el resultado
print("Conteo de eventos por tipo:")
print(df['Archive'].value_counts())
