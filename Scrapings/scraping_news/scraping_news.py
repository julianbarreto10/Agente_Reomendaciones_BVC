import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from Scrapings.scraping_news.news_obtain import news_obtain


# Función para obtener el contenido de un artículo
def extraer_contenido(url):
    try:
        # Encabezados personalizados para emular un navegador real
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()
        html = response.text

        soup = BeautifulSoup(html, 'html.parser')
        container = soup.find('div', class_='article-content')

        if container:
            contenido = ""
            for elemento in container.find_all(['p', 'h1', 'h2', 'h3', 'ul', 'ol', 'li']):
                contenido += elemento.get_text(strip=True) + "\n"
            return contenido
        return None
    except Exception as e:
        print(f"Error procesando {url}: {e}")
        return None

def scraping_news(date,stock):
    news_obtain(date,stock)
    # Cargar archivo CSV y una fecha de referencia
    df = pd.read_csv("Scrapings/scraping_news/news.csv")

    # Fecha de referencia (puedes cambiarla por cualquier otra)


    # Extraer contenido de los tres enlaces
    contenido_completo = ""
    number_news=0
    for index, row in df.iterrows():
        url = row['URL']  #
        number_news += 1
        contenido = extraer_contenido(url)
        if contenido:
            contenido_completo += f"--- Noticia relacionada {number_news} ---\n"
            contenido_completo += contenido + "\n\n"

    # Guardar el contenido en un archivo TXT
    ruta_archivo = os.path.join("agent_utils/docs_rag/", "news.txt")
    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(contenido_completo)

    print(f"Contenido extraído y guardado en {ruta_archivo}")
