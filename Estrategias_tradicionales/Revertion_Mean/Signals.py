import os
import pandas as pd
from Estrategias_tradicionales.Revertion_Mean.stock_information import stock_history

def revertion_mean(stock):
    # Llamada a la función para generar datos históricos
    stock_history(stock, "2023-06-06", "2025-01-01")

    # Nombre del archivo CSV
    csv_file = "Estrategias_tradicionales/Revertion_Mean/data_stock.csv"
    reversion_file = f"Resultados_Experimento/{stock}/reversion_signals.csv"

    # Verificar si el archivo existe
    if os.path.exists(csv_file):
        # Cargar los datos en un DataFrame
        df = pd.read_csv(csv_file, parse_dates=["Date"], index_col="Date")
        
        # Calcular la media móvil y la desviación estándar móvil
        window = 20  # Ventana de 20 días
        df['SMA_20'] = df['Close'].rolling(window=window).mean()
        df['STD_20'] = df['Close'].rolling(window=window).std()
        
        # Definir los límites para las señales
        df['Upper_Band'] = df['SMA_20'] + 2 * df['STD_20']  # Banda superior (2 desviaciones estándar)
        df['Lower_Band'] = df['SMA_20'] - 2 * df['STD_20']  # Banda inferior (2 desviaciones estándar)
        
        # Generar señales
        df['Signal'] = 'mantén'  # Por defecto, "mantener"
        df.loc[df['Close'] < df['Lower_Band'], 'Signal'] = 'compra'  # Precio bajo la banda inferior
        df.loc[df['Close'] > df['Upper_Band'], 'Signal'] = 'vende'   # Precio sobre la banda superior
        
        # Crear un DataFrame solo con las señales y guardarlo en un archivo CSV
        df_signals = df[['Close', 'SMA_20', 'Upper_Band', 'Lower_Band', 'Signal']].dropna()
        
        # Filtrar solo los datos del 2024 antes de guardar
        df_signals.index = pd.to_datetime(df_signals.index, utc=True).tz_convert(None)

        # Filtrar solo los datos del 2024 antes de guardar
        df_signals = df_signals[df_signals.index.year == 2024]
        df_signals.to_csv(reversion_file)
        
        print(f"Señales de reversión a la media generadas y guardadas en '{reversion_file}'.")
    else:
        print(f"El archivo '{csv_file}' no existe. Por favor, genera el archivo primero.")
