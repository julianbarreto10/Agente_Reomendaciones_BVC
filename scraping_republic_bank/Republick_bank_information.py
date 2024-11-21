import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL de la página de análisis de mercado en el blog de Tyba
url = "https://tyba.com.co/blog/category/analisis-de-mercado/"

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
    df = pd.DataFrame(data)

    # Imprimir el DataFrame
    print(df)
    df.to_csv("market_analysis.csv")

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")