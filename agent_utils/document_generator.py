from posixpath import join
import requests
from bs4 import BeautifulSoup

# URL del enlace
url = ['https://tyba.com.co/blog/analisis-de-mercado-semana-del-19-de-noviembre-2024/','https://www.banrep.gov.co/es/noticias/minutas-banrep-octubre-2024']

for i,j in enumerate(url):
  # Realiza la solicitud HTTP
  response = requests.get(j)

  # Si la respuesta es correcta (código de estado 200)
  if response.status_code == 200:
      # Parsear el contenido HTML de la página
      soup = BeautifulSoup(response.text, 'html.parser')

      # Abrir el archivo de texto para escribir
      with open('docs_rag/texto_extraido'+str(i)+'.txt', 'w', encoding='utf-8') as file:
          # Extraer los títulos
          titulos = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
          for titulo in titulos:
              file.write(f"Título: {titulo.get_text(strip=True)}\n\n")

          # Extraer los párrafos
          parrafos = soup.find_all('p')
          for parrafo in parrafos:
              file.write(f"{parrafo.get_text(strip=True)}\n\n")

      print("Texto extraído y guardado en 'texto_extraido"+str(i)+".txt'")
  else:
      print(f"Error al acceder al enlace: {response.status_code}")