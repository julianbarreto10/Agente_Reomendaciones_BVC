import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

csv_path = "scraping_news/news.csv"

def modificar_link(busqueda, fecha_inicio, fecha_fin):
    """
    Modifica el link de búsqueda basado en los parámetros proporcionados.

    Args:
        busqueda (str): Término de búsqueda (componente `q` en la URL).
        fecha_inicio (str): Fecha de inicio (componente `publishedAt[from]`).
        fecha_fin (str): Fecha de fin (componente `publishedAt[until]`).

    Returns:
        str: URL modificada con los nuevos parámetros.
    """
    base_url = "https://www.portafolio.co/buscar"
    params = {
        "q": busqueda,
        "sort_field": "publishedAt",
        "category": "",
        "publishedAt[from]": fecha_inicio,
        "publishedAt[until]": fecha_fin,
        "contentTypes[]": "article"
    }
    # Crear URL completa
    from urllib.parse import urlencode
    url_modificada = f"{base_url}?{urlencode(params)}"
    return url_modificada

def buscar_links(url):
    """
    Realiza la búsqueda en la URL proporcionada y extrae los enlaces dentro del contenido especificado.

    Args:
        url (str): URL de búsqueda.

    Returns:
        list: Lista de enlaces extraídos.
    """
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa
    if response.status_code != 200:
        print(f"Error al hacer la solicitud. Código de estado: {response.status_code}")
        return []

    # Analizar el HTML con BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Navegar por los elementos HTML
    main_container = soup.find("div", id="main-container")
    if not main_container:
        print("No se encontró el contenedor principal.")
        return []

    content_grid = main_container.find("div", class_="content_grid_home")
    if not content_grid:
        print("No se encontró la clase 'content_grid_home'.")
        return []

    search_results = content_grid.find("div", class_="search-results-container secondary-board")
    if not search_results:
        print("No se encontró la clase 'search-results-container secondary-board'.")
        return []

    default_listing = search_results.find("div", class_="default-listing")
    if not default_listing:
        print("No se encontró la clase 'default-listing'.")
        return []

    # Extraer los enlaces (href) de las divisiones
    links = []
    for div in default_listing.find_all("div", recursive=False):
        link = div.find("a", href=True)
        if link:
            links.append(link['href'])

    return links

# Ejemplo de uso
def news_obtain(date,stock):
    # Parámetros de entrada
    busqueda = stock
    # Fecha de inicio
    fecha_fin = date

    # Convertir fecha_inicio a un objeto datetime
    fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")

    # Restar dos semanas
    fecha_inicio = fecha_fin_dt - timedelta(weeks=2)
    fecha_inicio = str(fecha_inicio)

    data = []
    # Modificar el link
    url = modificar_link(busqueda, fecha_inicio, fecha_fin)
    print(f"URL generada: {url}")

    # Buscar enlaces
    enlaces = buscar_links(url)
    if enlaces:
        print("Enlaces encontrados:")
        for enlace in enlaces:
            print(f"https://www.portafolio.co/{enlace}")
            data.append({'URL': f"https://www.portafolio.co/{enlace}"})
        news_links = pd.DataFrame(data)
        news_links.to_csv(csv_path, index=False)
    else:
        print("No se encontraron enlaces.")