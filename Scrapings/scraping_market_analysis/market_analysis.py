import requests
from bs4 import BeautifulSoup
import pandas as pd
from Scrapings.scraping_market_analysis.Identificador_fecha import extraer_fecha_desde_link, convertir_fecha
import os

def actualizar_links_market_analisis():
    # URL de la página de análisis de mercado en el blog de Tyba
    url = "https://tyba.com.co/blog/category/analisis-de-mercado/"
    csv_path = "Scrapings/scraping_market_analysis/market_analysis.csv"

    # Hacer la solicitud GET a la página
    response = requests.get(url)

    # Verificar que la solicitud fue exitosa (código 200)
    if response.status_code == 200:
        # Crear el objeto BeautifulSoup para parsear el HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Buscar las secciones de los artículos (el selector puede variar)
        articles = soup.find_all('div', attrs={'data-post-id': True})

        # Lista para almacenar la información de los artículos
        data = []

        # Iterar sobre los artículos y extraer información
        for article in articles:
            overlay_div = article.find('div', class_='jet-engine-listing-overlay-wrap')
            if overlay_div and 'data-url' in overlay_div.attrs:
                # Extraer la URL desde el atributo `data-url`
                data_url = overlay_div['data-url']
                # Agregar el enlace al DataFrame
                data.append({'URL': data_url})

        # Crear un DataFrame con los datos
        new_links_df = pd.DataFrame(data)


        if os.path.exists(csv_path):
            # Leer el archivo existente
            existing_df = pd.read_csv(csv_path)

            # Combinar los nuevos enlaces con los existentes
            combined_df = pd.concat([existing_df, new_links_df], ignore_index=True)

            # Eliminar duplicados
            combined_df = combined_df.drop_duplicates(subset=['URL'], keep='first')

            # Guardar el archivo actualizado
            combined_df.to_csv(csv_path, index=False)
            print(f"El archivo '{csv_path}' ha sido actualizado con los nuevos enlaces.")
        else:
            # Si el archivo no existe, guardar los nuevos enlaces
            new_links_df.to_csv(csv_path, index=False)
            print(f"El archivo '{csv_path}' ha sido creado con los nuevos enlaces.")

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

    df = pd.read_csv("Scrapings/scraping_market_analysis/market_analysis.csv")

    # Identificar filas donde la columna 'Fecha' está vacía o es nula
    falta_fecha = df[df['Fecha'].isnull() | (df['Fecha'] == '')]

    # Procesar solo las filas que faltan fecha
    for index, row in falta_fecha.iterrows():
        url = row['URL']  # Reemplaza 'columna_con_links' con el nombre real de la columna
        fecha_texto = extraer_fecha_desde_link(url)
        if fecha_texto:
            fecha_formato = convertir_fecha(fecha_texto)
            df.at[index, 'Fecha'] = fecha_formato

    # Guardar el archivo actualizado
    df.to_csv("Scrapings/scraping_market_analysis/market_analysis.csv", index=False)

    print("Fechas faltantes completadas y guardadas en market_analysis_updated.csv")