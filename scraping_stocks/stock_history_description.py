import os
import pandas as pd
from stock_information import stock_history

stock_history("ECOPETROL.CL","2023-01-01","2023-11-19")
# Nombre del archivo CSV
csv_file = "data_stock.csv"
description_file = "stock_history_description.txt"

# Verificar si el archivo existe
if os.path.exists(csv_file):
    # Cargar los datos en un DataFrame
    df = pd.read_csv(csv_file, parse_dates=["Date"], index_col="Date")
    
    # Análisis de las características principales
    analysis = {}
    analysis['max_price'] = df['Close'].max()
    analysis['min_price'] = df['Close'].min()
    analysis['mean_price'] = df['Close'].mean()
    analysis['std_dev'] = df['Close'].std()
    analysis['total_volume'] = df['Volume'].sum()
    
    # Generar un resumen en lenguaje natural
    description = (
        f"Análisis del comportamiento de los precios de las acciones de ECOPETROL:\n\n"
        f"1. El precio máximo alcanzado fue de ${analysis['max_price']:.2f}.\n"
        f"2. El precio mínimo alcanzado fue de ${analysis['min_price']:.2f}.\n"
        f"3. El precio promedio durante el período fue de ${analysis['mean_price']:.2f}.\n"
        f"4. La volatilidad (desviación estándar) fue de ${analysis['std_dev']:.2f}.\n"
        f"5. El volumen total negociado en este período fue de {analysis['total_volume']:,} acciones.\n"
    )
    
    # Guardar la descripción en un archivo de texto
    with open(description_file, "w") as file:
        file.write(description)
    
    print(f"Análisis completado y guardado en '{description_file}'.")
else:
    print(f"El archivo '{csv_file}' no existe. Por favor, genera el archivo primero.")
