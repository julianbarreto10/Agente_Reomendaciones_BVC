import os
import pandas as pd
from Media_Movil.stock_information import stock_history

def movil_mean(stock):
    # Llamada a la función para generar datos históricos
    stock_history(stock, "2023-06-06", "2025-01-01")

    # Nombre del archivo CSV
    csv_file = "Media_Movil/data_stock.csv"
    signals_file = f"{stock}/SMA_signals.csv"

    # Verificar si el archivo existe
    if os.path.exists(csv_file):
        # Cargar los datos en un DataFrame
        df = pd.read_csv(csv_file, parse_dates=["Date"], index_col="Date")
        
        # Calcular las medias móviles
        df['SMA_10'] = df['Close'].rolling(window=10).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        
        # Generar señales de compra, venta o mantener
        df['Signal'] = 'mantén'  # Por defecto, "mantener"
        df.loc[df['SMA_10'] > df['SMA_50'], 'Signal'] = 'compra'
        df.loc[df['SMA_10'] < df['SMA_50'], 'Signal'] = 'vende'
        
        # Crear un DataFrame solo con las señales y guardarlo en un archivo CSV
        df_signals = df[['Close', 'SMA_10', 'SMA_50', 'Signal']].dropna()

        df_signals.index = pd.to_datetime(df_signals.index, utc=True).tz_convert(None)

        # Filtrar solo los datos del 2024 antes de guardar
        df_signals = df_signals[df_signals.index.year == 2024]
        df_signals.to_csv(signals_file)
        
        print(f"Señales de trading generadas y guardadas en '{signals_file}'.")
    else:
        print(f"El archivo '{csv_file}' no existe. Por favor, genera el archivo primero.")
