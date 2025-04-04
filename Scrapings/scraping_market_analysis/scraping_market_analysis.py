import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime


# Función para convertir una fecha de texto al formato de fecha
def convertir_a_fecha(fecha_texto):
    try:
        return datetime.strptime(fecha_texto, "%Y-%m-%d")
    except ValueError:
        print(f"Error al convertir la fecha: {fecha_texto}")
        return None

# Función para obtener el contenido de un artículo
def extraer_contenido(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        html = response.text

        soup = BeautifulSoup(html, 'html.parser')
        container = soup.find('div', class_='elementor-element elementor-element-61377f69 elementor-widget__width-initial elementor-widget elementor-widget-theme-post-content')

        if container:
            contenido = ""
            for elemento in container.find_all(['p', 'h1', 'h2', 'h3', 'ul', 'ol', 'li']):
                contenido += elemento.get_text(strip=True) + "\n"
            return contenido
        return None
    except Exception as e:
        print(f"Error procesando {url}: {e}")
        return None

def scraping_market_analysis(date):
    # Cargar archivo CSV y una fecha de referencia
    df = pd.read_csv("Scrapings/scraping_market_analysis/market_analysis.csv")
    df['Fecha'] = df['Fecha'].apply(convertir_a_fecha)  # Convertir fechas a formato datetime

    # Fecha de referencia (puedes cambiarla por cualquier otra)
    fecha_referencia = datetime.strptime(date, "%Y-%m-%d")

    # Encontrar los tres enlaces más cercanos por debajo de la fecha
    df_filtrado = df[df['Fecha'] < fecha_referencia].sort_values(by='Fecha', ascending=False).head(3)

    # Extraer contenido de los tres enlaces
    contenido_completo = ""
    for index, row in df_filtrado.iterrows():
        url = row['URL']  # Reemplaza 'columna_con_links' con el nombre correcto
        fecha = row['Fecha'].strftime("%Y-%m-%d")
        contenido = extraer_contenido(url)
        if contenido:
            contenido_completo += f"--- Artículo del {fecha} ---\n"
            contenido_completo += f"URL: {url}\n\n"
            contenido_completo += contenido + "\n\n"

    # Guardar el contenido en un archivo TXT
    ruta_archivo = os.path.join("agent_utils/docs_rag/", "market_analysis.txt")
    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(contenido_completo)

    print(f"Contenido extraído y guardado en {ruta_archivo}")
