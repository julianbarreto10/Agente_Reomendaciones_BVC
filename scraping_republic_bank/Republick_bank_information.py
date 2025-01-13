import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# URL de la página de análisis de mercado en el blog de Tyba
url = "https://www.banrep.gov.co/es/minutas"
csv_path = "scraping_republic_bank/Republic_bank.csv"



# Encabezados personalizados para emular un navegador real
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

# Hacer la solicitud GET a la página con los encabezados
response = requests.get(url, headers=headers)

# Verificar que la solicitud fue exitosa (código 200)
if response.status_code == 200:
    # Crear el objeto BeautifulSoup para parsear el HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Buscar las secciones de los artículos (el selector puede variar)
    rows = soup.find_all('tr')

    # Lista para almacenar la información de los artículos
    data = []

    # Iterar sobre los artículos y extraer información
    for row in rows:
        # Buscar la fecha en la etiqueta <time>
        time_tag = row.find('time')
        date = time_tag['datetime'][0:10] if time_tag else None

        # Buscar el enlace en la etiqueta <a>
        link_tag = row.find('a', href=True)
        href = "https://www.banrep.gov.co" + link_tag['href'] if link_tag else None

        # Solo agregar filas con datos completos
        if date and href:
            data.append({'URL': href,'Fecha': date})

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