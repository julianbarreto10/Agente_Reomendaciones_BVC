from agent import agent_bvc
from scraping_informes_bvc.data_obtain import descargar_y_procesar
import yfinance as yf



Fecha="2025-02-25"
stock="ecopetrol"
# Descargar y procesar informes de la BVC
descargar_y_procesar("ECOPETROL", "agent_utils/docs_rag/resumen_accion.txt")
respuesta=agent_bvc(Fecha,stock)
print(respuesta)

