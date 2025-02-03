import yfinance as yf
import pandas as pd


def stock_history(stock,start_date,end_date,tp=0):
    # Crear un objeto Ticker para la acción
    ticker = yf.Ticker(stock)

    # Descargar datos históricos, por ejemplo, desde enero de 2023 hasta noviembre de 2023
    data = ticker.history(start=start_date, end=end_date)

    # Asegurar que los datos están en un DataFrame (esto ya es un DataFrame por defecto)
    df = pd.DataFrame(data)
    # Obtener la última fila sin la columna Date
    last_row = df.iloc[-1, :]

    # Crear la descripción
    descripcion = (
        f"Ten en cuenta que para el día anterior la acción tuvo estos valores: "
        f"apertura en {last_row['Open']}, un máximo de {last_row['High']}, un mínimo de {last_row['Low']}, "
        f"cerró en {last_row['Close']}, con un volumen de {last_row['Volume']}, "
        f"dividendos de {last_row['Dividends']} y {last_row['Stock Splits']} divisiones de acciones."
    )

    # Guardar la descripción en un archivo
    with open("scraping_stocks/info_accion.txt", "w") as file:
        file.write(descripcion)

    # Exportar a un archivo CSV
    if tp==0:
        df.to_csv("scraping_stocks/data_stock.csv")
    else:
        df.to_csv(stock+"/data_stock.csv")