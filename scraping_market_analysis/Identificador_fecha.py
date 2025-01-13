import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

# Leer el archivo CSV
df = pd.read_csv("scraping_market_analysis/market_analysis.csv")

# Función para extraer la fecha desde el contenido HTML de un enlace
def extraer_fecha_desde_link(url):
    try:
        # Hacer una solicitud al enlace
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        html = response.text

        # Analizar el HTML con BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Buscar el bloque donde está la fecha
        div_bio = soup.find('div', class_='elementor-author-box__bio')

        if div_bio:
            # Extraer el texto dentro del div y buscar la fecha con Regex
            texto = div_bio.get_text(strip=True)
            patron = r"(\d{1,2} de \w+ , \d{4})"
            match = re.search(patron, texto)
            if match:
                return match.group(1)
        return None
    except Exception as e:
        print(f"Error procesando {url}: {e}")
        return None

# Función para convertir la fecha al formato YYYY-MM-DD
def convertir_fecha(fecha_texto):
    try:
        # Diccionario de traducción de meses en español
        meses = {
            "enero": "01", "febrero": "02", "marzo": "03", "abril": "04",
            "mayo": "05", "junio": "06", "julio": "07", "agosto": "08",
            "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12"
        }
        # Extraer partes de la fecha
        patron = r"(\d{1,2}) de (\w+) , (\d{4})"
        match = re.search(patron, fecha_texto)
        if match:
            dia, mes, anio = match.groups()
            mes_num = meses[mes.lower()]  # Convertir mes a número
            return f"{anio}-{mes_num.zfill(2)}-{dia.zfill(2)}"
        return None
    except Exception as e:
        print(f"Error convirtiendo la fecha {fecha_texto}: {e}")
        return None

# Aplicar la extracción y conversión a cada enlace
# Reemplaza 'columna_con_links' con el nombre de la columna que contiene los enlaces
df['Fecha'] = df['URL'].apply(extraer_fecha_desde_link)
df['Fecha'] = df['Fecha'].apply(lambda x: convertir_fecha(x) if x else None)

# Guardar el resultado en un nuevo archivo CSV
df.to_csv("scraping_market_analysis/market_analysis.csv", index=False)

print("Fechas extraídas, convertidas y guardadas en market_analysis_with_dates.csv")
