from bs4 import BeautifulSoup
import pandas as pd
import os

# Ruta del archivo de texto con código HTML
file_path = "Scrapings/scraping_market_analysis/market_analysis.txt"
# Ruta del archivo CSV
csv_path = "Scrapings/scraping_market_analysis/market_analysis.csv"

# Lista para almacenar los enlaces extraídos
data = []

# Enlace a excluir
exclude_url = "https://tyba.com.co/blog/category/analisis-de-mercado/"

try:
    # Leer el contenido del archivo HTML
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Crear el objeto BeautifulSoup para parsear el HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Buscar todas las etiquetas <a> con atributo href
    links = soup.find_all('a', href=True)

    # Extraer los enlaces y almacenarlos en la lista
    for link in links:
        href = link['href']
        if href != exclude_url:  # Omitir el enlace específico
            data.append({'URL': href})

    # Crear un DataFrame con los nuevos enlaces
    new_links_df = pd.DataFrame(data)

    # Verificar si el archivo CSV ya existe
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

except FileNotFoundError:
    print(f"No se encontró el archivo '{file_path}'. Asegúrate de que el archivo exista y la ruta sea correcta.")
