import os
import pandas as pd
from Scrapings.scraping_stocks.stock_information import stock_history
from datetime import datetime, timedelta


def scraping_stocks(date,stock):
    end_date = datetime.strptime(date, "%Y-%m-%d")

    date_ranges = {
        'año': end_date.replace(year=end_date.year - 1),  # Hace un año
        'mes': (end_date - timedelta(days=30)),        # Hace 30 días (aproximadamente un mes)
        'semana': (end_date - timedelta(weeks=1))          # Hace 7 días
    }

    final_description=""

    for report in ['año', 'mes', 'semana']:
        start_date = date_ranges[report]
        data = {
            "stock": ["ecopetrol", "bancolombia", "nutresa", "cemargos"],
            "real_name": ["ECOPETROL.CL", "PFBCOLOM.CL", "NUTRESA.CL", "CEMARGOS.CL"]
        }

        df_stocks = pd.DataFrame(data)


        # Obtener el nombre real de la acción
        stock_real_name = df_stocks.set_index("stock")["real_name"].to_dict().get(stock, stock)

        # Llamada a la función para generar datos históricos
        stock_history(stock_real_name, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))

        # Nombre del archivo CSV y el archivo de descripción
        csv_file = "Scrapings/scraping_stocks/data_stock.csv"
        description_file = "agent_utils/docs_rag/stock_history_description.txt"

        # Verificar si el archivo existe
        if os.path.exists(csv_file):
            # Cargar los datos en un DataFrame
            df = pd.read_csv(csv_file, parse_dates=["Date"], index_col="Date")
            
            # Calcular métricas básicas
            analysis = {
                'max_price': df['Close'].max(),
                'min_price': df['Close'].min(),
                'mean_price': df['Close'].mean(),
                'std_dev': df['Close'].std(),
                'total_volume': df['Volume'].sum(),
            }
            
            # Calcular promedios móviles
            df['SMA_10'] = df['Close'].rolling(window=10).mean()
            df['SMA_50'] = df['Close'].rolling(window=50).mean()
            df['SMA_200'] = df['Close'].rolling(window=200).mean()
            
            # Calcular el rango promedio verdadero (ATR)
            df['High-Low'] = df['High'] - df['Low']
            df['High-Close'] = abs(df['High'] - df['Close'].shift())
            df['Low-Close'] = abs(df['Low'] - df['Close'].shift())
            df['TR'] = df[['High-Low', 'High-Close', 'Low-Close']].max(axis=1)
            df['ATR'] = df['TR'].rolling(window=14).mean()
            
            # Identificar días con movimientos extremos
            max_increase_day = df['Close'].diff().idxmax()
            max_decrease_day = df['Close'].diff().idxmin()
            
            # Generar el análisis en lenguaje natural
            description = (
                f"Análisis del comportamiento del ultimo {report} de los precios de las acciones de {stock_real_name}:\n\n"
                f"1. El precio máximo alcanzado fue de ${analysis['max_price']:.2f}.\n"
                f"2. El precio mínimo alcanzado fue de ${analysis['min_price']:.2f}.\n"
                f"3. El precio promedio durante el período fue de ${analysis['mean_price']:.2f}.\n"
                f"4. La volatilidad (desviación estándar) fue de ${analysis['std_dev']:.2f}.\n"
                f"5. El volumen total negociado en este período fue de {analysis['total_volume']:,} acciones.\n\n"
                f"Promedios móviles:\n"
                f" - SMA 10 días: ${df['SMA_10'].iloc[-1]:.2f}\n"
                f" - SMA 50 días: ${df['SMA_50'].iloc[-1]:.2f}\n"
                f" - SMA 200 días: ${df['SMA_200'].iloc[-1]:.2f}\n\n"
                f"Volatilidad diaria (ATR): ${df['ATR'].iloc[-1]:.2f}\n\n"
                f"Días de movimientos extremos:\n"
                f" - Mayor aumento en precio: {max_increase_day.date()} (${df['Close'].loc[max_increase_day]:.2f})\n"
                f" - Mayor caída en precio: {max_decrease_day.date()} (${df['Close'].loc[max_decrease_day]:.2f})\n\n"
            )

            final_description+=description
    # Guardar el análisis en el archivo de texto
    with open(description_file, "w") as file:
        file.write(final_description)
            
    print(f"Análisis completado y guardado en '{description_file}'.")
    