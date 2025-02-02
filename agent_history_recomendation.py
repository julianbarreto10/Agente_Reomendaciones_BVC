from agent import agent_bvc
from scraping_stocks.stock_information import stock_history
from datetime import datetime, timedelta
import pandas as pd
import os
from Revertion_Mean.Signals import revertion_mean
from Media_Movil.Signals import movil_mean
from buy_mantein.Signals import buy_mantein

Fecha="2025-01-01"
end_date = datetime.strptime(Fecha, "%Y-%m-%d")
start_date = end_date.replace(year=end_date.year - 1)
stock="nutresa"
data = {
        "stock": ["ecopetrol", "bancolombia", "nutresa", "cemargos"],
        "real_name": ["ECOPETROL.CL", "BANCOLOMBIA.CL", "NUTRESA.CL", "CEMARGOS.CL"]
    }

df_stocks = pd.DataFrame(data)


# Obtener el nombre real de la acción
stock_real_name = df_stocks.set_index("stock")["real_name"].to_dict().get(stock, stock)
revertion_mean(stock_real_name)
movil_mean(stock_real_name)
buy_mantein(stock_real_name)
stock_history(stock_real_name, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'),1)
#respuesta=agent_bvc(Fecha,stock)
#print(respuesta)


def obtener_sugerencia(respuesta):
    opciones = ["compra", "vende", "mantén"]
    for opcion in opciones:
        if opcion in respuesta.lower():
            return opcion
    print(f"No se identificó una sugerencia en la respuesta: {respuesta}")
    return input("Ingrese manualmente la sugerencia (compra/vende/mantén): ")

def procesar_stock(stock_real_name, stock):
    archivo_csv = os.path.join(stock_real_name, "data_stock.csv")
    archivo_salida = os.path.join(stock_real_name, "sugerencias.csv")
    
    if not os.path.exists(archivo_csv):
        print(f"El archivo {archivo_csv} no existe.")
        return
    
    df = pd.read_csv(archivo_csv)
    if os.path.exists(archivo_salida):
        df_existente = pd.read_csv(archivo_salida)
        df["sugerencia"] = df_existente["sugerencia"]
        df_existente = df_existente[df_existente.sugerencia.notna()]
        fechas_procesadas = set(df_existente["Date"])
    else:
        fechas_procesadas = set()
        df["sugerencia"] = df.get("sugerencia", "")
    for i, row in df.iterrows():
        if row["Date"] in fechas_procesadas:
            continue
        
        Fecha = datetime.strptime(row["Date"].split()[0], "%Y-%m-%d")
        Fecha = str(Fecha)[0:10]
        print(Fecha)
        respuesta = agent_bvc(Fecha, stock)
        sugerencia = obtener_sugerencia(respuesta)
        df.at[i, "sugerencia"] = sugerencia
        df.to_csv(archivo_salida, index=False)
        print(f"Guardado en {archivo_salida}: {Fecha} - {sugerencia}")
    
    print("Proceso completado.")

# Ejemplo de uso

procesar_stock(stock_real_name, stock)