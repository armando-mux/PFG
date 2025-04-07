import pandas as pd

pd.options.display.max_columns = None

# Cargar el archivo CSV en un DataFrame
df = pd.read_csv('filesystem_event.csv')

# Verificar los primeros registros para saber cómo está estructurado el archivo
print(df.head())

# Especificamos el nombre del campo que queremos analizar (en este caso 'evento')
campo = 'Event'

# Contar los valores únicos en el campo especificado
conteo_eventos = df[campo].value_counts()

# Mostrar el resultado
print("Conteo de eventos por tipo:")
print(conteo_eventos)
