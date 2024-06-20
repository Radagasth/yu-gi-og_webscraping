from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

# Configuración de Selenium con Chrome
service = Service('C:/Users/siste/OneDrive/Escritorio/chromedriver-win32/chromedriver.exe')
driver = webdriver.Chrome(service=service)

# URL de la página web que contiene la tabla
url = 'https://ygoprodeck.com/tournaments/'
driver.get(url)

# Inicializar una lista para almacenar los datos
data = []

# Función para extraer datos de la tabla
def extraer_datos():
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', id='tournamentsTable')
    if table:
        rows = table.find('tbody').find_all('tr')
        print(f"Se encontraron {len(rows)} filas en la tabla.")
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 6:
                fecha = cells[0].text.strip()
                pais = cells[1].text.strip()
                nombre_torneo = cells[2].find('a').text.strip()
                url_torneo = cells[2].find('a')['href']
                jugadores = cells[3].text.strip()
                ganador = cells[4].text.strip()
                formato = cells[5].text.strip()
                data.append([fecha, nombre_torneo, url_torneo, jugadores, ganador, formato])

# Esperar hasta que la tabla esté presente y cargar la primera página
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'tournamentsTable')))
time.sleep(10)
extraer_datos()

# Ciclo para cambiar de página y extraer datos
for _ in range(33):  # Cambia de página 10 veces
    try:
        # Encontrar el enlace de "Siguiente" dentro del elemento de lista
        next_button_li = driver.find_element(By.ID, 'tournamentsTable_next')
        next_button_a = next_button_li.find_element(By.TAG_NAME, 'a')
        
        if "disabled" not in next_button_li.get_attribute('class'):  # Verificar si el botón no está deshabilitado
            driver.execute_script("arguments[0].scrollIntoView();", next_button_a)  # Desplazar el enlace a la vista
            time.sleep(2)  # Esperar un momento para asegurar que el desplazamiento se ha completado
            driver.execute_script("arguments[0].click();", next_button_a)  # Hacer clic usando JavaScript
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'tournamentsTable')))
            time.sleep(10)  # Esperar para asegurar que la página se ha cargado completamente
            extraer_datos()
        else:
            print("Botón 'Siguiente' deshabilitado, terminando el ciclo.")
            break
    except Exception as e:
        print(f"Error al cambiar de página: {e}")
        break

# Cerrar el navegador
driver.quit()

# Crear un DataFrame de pandas con los datos
df = pd.DataFrame(data, columns=['Fecha', 'Nombre del Torneo', 'URL del Torneo', 'Jugadores', 'Ganador', 'Formato'])

# Guardar los datos en un archivo Excel
df.to_excel('torneos.xlsx', index=False)

print("Datos extraídos y guardados en torneos.xlsx")
