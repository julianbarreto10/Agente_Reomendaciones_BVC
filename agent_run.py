from agent import agent_bvc
from Scrapings.scraping_informes_bvc.data_obtain import descargar_y_procesar
import yfinance as yf
from Scrapings.scraping_republic_bank.Republick_bank_information import actualizar_links_republic_bank
from Scrapings.scraping_market_analysis.market_analysis import actualizar_links_market_analisis

# Fecha y accion a analizar
# Fecha en formato YYYY-MM-DD
Fecha="2025-04-04"
stock="ecopetrol"

actualizar_links_market_analisis() #No es necesario actualizar cada vez, los informes salen cada semana
actualizar_links_republic_bank() #No es necesario actualizar cada vez, los informes salen cada mes

# Descargar y procesar informes de la BVC, aplica solo para la fecha actual o hasta tres dias antes
# de lo contrrio comentariar la siguiente linea de codigo
descargar_y_procesar("ECOPETROL", "agent_utils/docs_rag/resumen_accion.txt")

# Correr Agente_BVC
respuesta=agent_bvc(Fecha,stock)
print(respuesta)

