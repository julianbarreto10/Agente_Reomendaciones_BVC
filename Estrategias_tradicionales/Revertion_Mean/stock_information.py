import yfinance as yf
import pandas as pd


def stock_history(stock,start_date,end_date):
    # Crear un objeto Ticker para accion
    ticker = yf.Ticker(stock)

    # Descargar datos históricos, por ejemplo, desde enero de 2023 hasta noviembre de 2023
    data = ticker.history(start=start_date, end=end_date)

    # Asegurar que los datos están en un DataFrame (esto ya es un DataFrame por defecto)
    df = pd.DataFrame(data)

    # Exportar a un archivo CSV
    df.to_csv("Estrategias_tradicionales/Revertion_Mean/data_stock.csv")