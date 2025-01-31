import os
import pandas as pd
from stock_information import stock_history

# Llamada a la función para generar datos históricos
stock_history("ECOPETROL.CL", "2024-01-01", "2024-12-31")

# Nombre del archivo CSV
csv_file = "buy_mantein/data_stock.csv"
reversion_file = "buy_mantein/reversion_signals.csv"

# Verificar si el archivo existe
if os.path.exists(csv_file):
    # Cargar los datos en un DataFrame
    df = pd.read_csv(csv_file)
    df["Signal"]="Comprar"
    df_signals=df
    df_signals.to_csv(reversion_file)
    
    print(f"Señales de reversión a la media generadas y guardadas en '{reversion_file}'.")
else:
    print(f"El archivo '{csv_file}' no existe. Por favor, genera el archivo primero.")
