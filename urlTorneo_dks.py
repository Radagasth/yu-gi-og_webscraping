import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Leer el archivo Excel
df = pd.read_excel('C:/Users/siste/OneDrive/Escritorio/torneos.xlsx')  # Reemplaza con la ruta a tu archivo Excel

# Número máximo de torneos a visitar
max_torneos = 1700

# Filtrar solo los primeros 10 torneos
df = df.head(max_torneos)

# Configuración de Selenium con Chrome
service = Service('C:/Users/siste/OneDrive/Escritorio/chromedriver-win32/chromedriver.exe')
driver = webdriver.Chrome(service=service)

# Lista para almacenar los datos extraídos
data = []

# Iterar sobre cada URL en el archivo Excel
for index, row in df.iterrows():
    base_url = "https://ygoprodeck.com"
    tournament_url = row['URL del Torneo']
    full_url = base_url + tournament_url
    
    # Visitar la URL
    driver.get(full_url)
    
    # Esperar hasta que algún contenido específico esté presente
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'tournament_table'))
        )
        time.sleep(10)  # Esperar un poco más para asegurar que todo el contenido se ha cargado

        # Obtener el HTML de la página cargada
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extraer datos específicos de la página
        tournament_name = row['Nombre del Torneo']
        tournament_date = row['Fecha']
        tournament_winner = row['Ganador']
        tournament_players = row['Jugadores']
        
        # Encontrar todas las filas con href en tournament_table_row
        rows = soup.find_all('a', class_='tournament_table_row', href=True)
        for row in rows:
            deck_url = base_url + row['href']
            data.append([tournament_date, tournament_name, full_url, tournament_players, tournament_winner, deck_url])
    
    except Exception as e:
        print(f"Error al procesar la URL {full_url}: {e}")
        continue

# Cerrar el navegador
driver.quit()

# Crear un DataFrame de pandas con los datos extraídos
df_result = pd.DataFrame(data, columns=['Fecha', 'Nombre del Torneo', 'URL del Torneo', 'Jugadores', 'Ganador', 'URL del Deck'])

# Guardar los datos en un archivo Excel
df_result.to_excel('decks.xlsx', index=False)

print("Datos extraídos y guardados en decks.xlsx")
