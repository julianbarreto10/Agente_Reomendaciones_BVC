import pandas as pd
import numpy as np
import yfinance as yf
import scipy.stats as stats
import matplotlib.pyplot as plt

# Rutas de los archivos CSV
archivos = {
    "Buy_Mantein": "buy_mantein/reversion_signals.csv",
    "Revertion_Mean": "Revertion_Mean/reversion_signals.csv",
    "Media_Movil": "Media_Movil/trading_signals.csv",
    "Agente_BVC": "ECOPETROL.CL/sugerencias.csv",
}

# Nombre de la columna de sugerencias (varía por archivo)
columna_sugerencia = {
    "Buy_Mantein": "Signal",
    "Revertion_Mean": "Signal",
    "Media_Movil": "Signal",
    "Agente_BVC": "sugerencia",
}

# Índice de referencia (ejemplo: S&P 500)
indice_referencia = "ECOPETROL.CL"

# Tasa libre de riesgo (ejemplo: 5%)
tasa_libre_riesgo = 0.05

# DataFrame para guardar los resultados
resultados = pd.DataFrame()

# Función para calcular métricas
def calcular_metricas(df, nombre_activo, columna_sugerencia):
    # Calcular rendimiento diario
    df['Rendimiento Diario'] = 0.0
    for i in range(1, len(df)):
        if df[columna_sugerencia][i] == 'comprar':
            df['Rendimiento Diario'][i] = (df['Close'][i] - df['Close'][i-1]) / df['Close'][i-1]
        elif df[columna_sugerencia][i] == 'vender':
            df['Rendimiento Diario'][i] = -(df['Close'][i] - df['Close'][i-1]) / df['Close'][i-1]

    # Calcular ARR
    rendimiento_promedio_diario = df['Rendimiento Diario'].mean()
    ARR = (1 + rendimiento_promedio_diario)**252 - 1

    # Calcular volatilidad
    volatilidad_diaria = df['Rendimiento Diario'].std()
    volatilidad_anual = volatilidad_diaria * np.sqrt(252)

    # Calcular Sharpe Ratio
    sharpe_ratio = (ARR - tasa_libre_riesgo) / volatilidad_anual

    return ARR, volatilidad_anual, sharpe_ratio

# Leer datos y calcular métricas para cada activo
for nombre_activo, ruta_archivo in archivos.items():
    df = pd.read_csv(ruta_archivo, parse_dates=['Date'], index_col='Date')
    ARR, volatilidad, sharpe_ratio = calcular_metricas(df, nombre_activo, columna_sugerencia[nombre_activo])
    resultados.loc[nombre_activo, 'ARR'] = ARR
    resultados.loc[nombre_activo, 'Volatilidad'] = volatilidad
    resultados.loc[nombre_activo, 'Sharpe Ratio'] = sharpe_ratio

# Obtener datos del índice de referencia
df_indice = pd.read_csv("ECOPETROL.CL/data_stock.csv")

# Calcular métricas para el índice de referencia
ARR_indice, volatilidad_indice, sharpe_ratio_indice = calcular_metricas(df_indice, "Índice de referencia", "N/A")
resultados.loc["Índice de referencia", 'ARR'] = ARR_indice
resultados.loc["Índice de referencia", 'Volatilidad'] = volatilidad_indice
resultados.loc["Índice de referencia", 'Sharpe Ratio'] = sharpe_ratio_indice

# Análisis estadístico
print("\nAnálisis estadístico:")
for metrica in ['ARR', 'Volatilidad', 'Sharpe Ratio']:
    fvalue, pvalue = stats.f_oneway(
        resultados.loc['Activo1', metrica],
        resultados.loc['Activo2', metrica],
        resultados.loc['Activo3', metrica],
        resultados.loc['Activo4', metrica],
        resultados.loc['Índice de referencia', metrica]
    )
    print(f"Prueba ANOVA para {metrica}: F = {fvalue:.2f}, p = {pvalue:.3f}")

# Gráficos
fig, axes = plt.subplots(3, 1, figsize=(10, 15))

resultados.plot(y='ARR', kind='bar', ax=axes[0])
axes[0].set_title('ARR')

resultados.plot(y='Volatilidad', kind='bar', ax=axes[1])
axes[1].set_title('Volatilidad')

resultados.plot(y='Sharpe Ratio', kind='bar', ax=axes[2])
axes[2].set_title('Sharpe Ratio')

plt.tight_layout()
plt.show()