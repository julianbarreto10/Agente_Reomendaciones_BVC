import pandas as pd
import numpy as np

# Indice de referencia para calculo métricas
# puede ser CEMARGOS.CL o ECOPETROL.CL o PFBCOLOM.CL o NUTRESA.CL.
indice_referencia = "CEMARGOS.CL"

# Rutas de los archivos CSV
archivos = {
    "Buy_Mantein": f"Resultados_Experimento/{indice_referencia}/buy_mantein_signals.csv",
    "Revertion_Mean": f"Resultados_Experimento/{indice_referencia}/reversion_signals.csv",
    "Media_Movil": f"Resultados_Experimento/{indice_referencia}/SMA_signals.csv",
    "Agente_BVC": f"Resultados_Experimento/{indice_referencia}/agente_signals.csv",
}

# Nombre de la columna de sugerencias (varía por archivo)
columna_sugerencia = {
    "Buy_Mantein": "Signal",
    "Revertion_Mean": "Signal",
    "Media_Movil": "Signal",
    "Agente_BVC": "sugerencia",
}



# Tasa libre de riesgo (ejemplo: 5%)
tasa_libre_riesgo = 0.05

# DataFrame para guardar los resultados
resultados = pd.DataFrame()
df_indice = pd.read_csv(f"Resultados_Experimento/{indice_referencia}/data_stock.csv")
# Función para calcular métricas
def calcular_metricas(df, nombre_activo, columna_sugerencia, df_indice):
    # Calcular rendimiento diario
    df['Rendimiento Diario'] = 0.0
    for i in range(1, len(df)):
        if df[columna_sugerencia][i] == 'compra':
            df['Rendimiento Diario'][i] = (df['Close'][i] - df['Close'][i-1]) / df['Close'][i-1]
        elif df[columna_sugerencia][i] == 'vende':
            df['Rendimiento Diario'][i] = -(df['Close'][i] - df['Close'][i-1]) / df['Close'][i-1]
    df_indice[nombre_activo]=list(df[columna_sugerencia])
    Rendimiento=nombre_activo+'_Rnd'
    df_indice[Rendimiento]=list(df['Rendimiento Diario'])
        
    # Calcular ARR
    rendimiento_promedio_diario = df['Rendimiento Diario'].mean()
    ARR = (1 + rendimiento_promedio_diario)**253 - 1

    # Calcular volatilidad
    volatilidad_diaria = df['Rendimiento Diario'].std()
    volatilidad_anual = volatilidad_diaria * np.sqrt(253)

    # Calcular Sharpe Ratio
    sharpe_ratio = (ARR - tasa_libre_riesgo) / volatilidad_anual

    return ARR, volatilidad_anual, sharpe_ratio, df_indice



# Leer datos y calcular métricas para cada activo
for nombre_activo, ruta_archivo in archivos.items():
    df = pd.read_csv(ruta_archivo, parse_dates=['Date'], index_col='Date')
    print(df.head(5))
    ARR, volatilidad, sharpe_ratio, df_indice = calcular_metricas(df, nombre_activo, columna_sugerencia[nombre_activo], df_indice)
    resultados.loc[nombre_activo, 'ARR'] = ARR
    resultados.loc[nombre_activo, 'Volatilidad'] = volatilidad
    resultados.loc[nombre_activo, 'Sharpe Ratio'] = sharpe_ratio

resultados.to_csv(f"Resultados_Experimento/{indice_referencia}/tabla_resultados.csv")
df_indice.to_csv(f"Resultados_Experimento/{indice_referencia}/stock_sugerencias.csv")