import os
import zipfile
import pandas as pd

# Ruta de la carpeta que contiene los archivos ZIP
zip_folder = "scraping_informes_bvc"

# Nombre de la hoja que deseas convertir a DataFrame
sheet_name = "Hoja1"  # Cambia esto según el nombre de la hoja en el Excel

# Lista para almacenar DataFrames extraídos
dataframes = []

# Verificar si la carpeta existe
if os.path.exists(zip_folder):
    # Recorrer todos los archivos en la carpeta
    for file_name in os.listdir(zip_folder):
        file_path = os.path.join(zip_folder, file_name)
        
        # Verificar si el archivo es un ZIP
        if zipfile.is_zipfile(file_path):
            # Crear una carpeta temporal para extraer los archivos
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                extract_folder = os.path.join(zip_folder, "temp_extracted")
                zip_ref.extractall(extract_folder)
                
                # Buscar archivos Excel en la carpeta extraída
                for extracted_file in os.listdir(extract_folder):
                    if extracted_file.endswith(".xlsx") or extracted_file.endswith(".xls"):
                        excel_path = os.path.join(extract_folder, extracted_file)
                        
                        # Leer la hoja específica del archivo Excel
                        try:
                            df = pd.read_excel(excel_path, sheet_name=sheet_name)
                            dataframes.append(df)
                            print(f"DataFrame extraído de {extracted_file}.")
                        except Exception as e:
                            print(f"No se pudo leer la hoja '{sheet_name}' de {extracted_file}: {e}")
                
                # Limpiar la carpeta temporal
                for extracted_file in os.listdir(extract_folder):
                    os.remove(os.path.join(extract_folder, extracted_file))
                os.rmdir(extract_folder)
else:
    print(f"La carpeta '{zip_folder}' no existe. Por favor verifica la ruta.")

# Combinar los DataFrames (si es necesario)
if dataframes:
    combined_df = pd.concat(dataframes, ignore_index=True)
    print("Se han combinado todos los DataFrames extraídos.")
else:
    print("No se encontraron archivos Excel o no se pudieron leer.")
