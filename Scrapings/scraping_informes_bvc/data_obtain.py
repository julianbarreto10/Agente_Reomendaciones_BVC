import os
import time
import zipfile
import shutil
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def descargar_y_procesar(accion, salida_txt):
    # Configuración de Selenium
    download_dir = os.path.abspath("Scrapings/scraping_informes_bvc/Informes_BVC")
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Configuración de opciones de Chrome para gestionar las descargas.
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    # Inicializar el controlador de Selenium.
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Acceder a la página de informes bursátiles.
        url_pagina = "https://www.bvc.com.co/informes-y-boletines?tab=informes-bursatiles_diario"
        driver.get(url_pagina)
        
        # Esperar y hacer clic en el botón de descarga.
        wait = WebDriverWait(driver, 20)
        boton_descarga = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "download-block__icon")))
        boton_descarga.click()
        
        # Esperar a que la descarga se complete.
        time.sleep(10)
        archivos = [f for f in os.listdir(download_dir) if f.endswith('.zip')]
        if not archivos:
            print("No se encontró el archivo ZIP después de la descarga.")
            return
        
        # Extraer el contenido del archivo ZIP.
        archivo_zip = os.path.join(download_dir, archivos[0])
        with zipfile.ZipFile(archivo_zip, 'r') as zip_ref:
            zip_ref.extractall(download_dir)
            nombres_archivos = zip_ref.namelist()
        
        # Identificar la carpeta extraída y el archivo Excel dentro de ella.
        carpetas_extraidas = [f for f in os.listdir(download_dir) if os.path.isdir(os.path.join(download_dir, f))]
        if not carpetas_extraidas:
            print("No se encontró ninguna carpeta en el ZIP.")
            return
        
        carpeta_raiz = os.path.join(download_dir, carpetas_extraidas[0])
        archivo_excel = next((f for f in os.listdir(carpeta_raiz) if f.endswith('.xlsx')), None)
        if not archivo_excel:
            print("No se encontró archivo Excel en la carpeta extraída.")
            return
        
        # Leer el archivo Excel y detectar la tabla de datos.
        df = pd.read_excel(os.path.join(carpeta_raiz, archivo_excel), sheet_name="RV-Indicadores", engine="openpyxl", header=None)
        
        # Buscar la fila donde comienza la tabla.
        for i, row in df.iterrows():
            if "Nemotécnico / Ticker" in row.values:
                df.columns = df.iloc[i]
                df = df[i+1:].reset_index(drop=True)
                break
        
        # Filtrar los datos por la acción especificada.
        df_filtrado = df[df["Nemotécnico / Ticker"] == accion]
        if df_filtrado.empty:
            print(f"No se encontraron datos para la acción: {accion}")
            return
        
        # Generar un resumen con los datos relevantes de la acción.
        resumen = f"Resumen de la acción {accion}\n"
        resumen += df_filtrado.to_string(index=False)
        resumen += "\n\nAnálisis:\n"
        resumen += f"Variación diaria: {df_filtrado['Var. % Diaria / Daily'].values[0]}%\n"
        resumen += f"Variación mensual: {df_filtrado['Var. % Mes / Month'].values[0]}%\n"
        resumen += f"Variación anual: {df_filtrado['Var. % Anual / Annual'].values[0]}%\n"
        resumen += f"Rendimiento YTD: {df_filtrado['YTD'].values[0]}%\n"
        resumen += f"Dividendo: {df_filtrado['Dividendo / Dividend'].values[0]}\n"
        resumen += f"Valor en libros: {df_filtrado['Valor en Libros / Book Value'].values[0]} (Fecha: {df_filtrado['Fecha Valor en Libros / Date Book Value'].values[0]})\n"
        resumen += f"Utilidad por acción: {df_filtrado['Utilidad por Acción / Earnings per Share'].values[0]}\n"
        resumen += f"Yield: {df_filtrado['YIELD'].values[0]}\n"
        resumen += f"Q Tobin: {df_filtrado['QTOBIN'].values[0]}\n"
        resumen += f"RPG: {df_filtrado['RPG'].values[0]}\n"
        
        # Guardar el resumen en un archivo de texto.
        with open(salida_txt, 'w', encoding='utf-8') as f:
            f.write(resumen)
        
        print(f"Archivo de resumen generado: {salida_txt}")

    finally:
        driver.quit()
        # Eliminar todos los archivos y carpetas en la carpeta de descargas.
        for archivo in os.listdir(download_dir):
            ruta_archivo = os.path.join(download_dir, archivo)
            try:
                if os.path.isdir(ruta_archivo):
                    shutil.rmtree(ruta_archivo)
                else:
                    os.remove(ruta_archivo)
            except Exception as e:
                print(f"No se pudo eliminar {ruta_archivo}: {e}")


# Uso de la función
# descargar_y_procesar("BCOLOMBIA", "agent_utils/docs_rag/resumen_accion.txt")