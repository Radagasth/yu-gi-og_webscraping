import requests
from bs4 import BeautifulSoup
import pandas as pd

# Leer URLs desde el archivo de Excel
urls_df = pd.read_excel('C:/Users/siste/OneDrive/Escritorio/decks.xlsx')  # Reemplaza con la ruta a tu archivo Excel

# Inicializar una lista para almacenar los DataFrames de cada mazo
all_decks_data = []

# Función para obtener los datos del mazo desde una URL
def obtener_datos_mazo(url):
    # Realizar la solicitud HTTP para obtener el contenido HTML de la página
    response = requests.get(url)
    html_content = response.content

    # Crear un objeto BeautifulSoup para analizar el HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Secciones del mazo que se van a buscar
    sections = {
        'Main Deck': 'main_deck',
        'Extra Deck': 'extra_deck',
        'Side Deck': 'side_deck'
    }

    # Inicializar un diccionario para almacenar la información de las cartas por sección
    deck_data = {section: [] for section in sections}

    # Recorrer cada sección del mazo
    for section_name, section_id in sections.items():
        # Encontrar la sección que contiene las cartas del mazo
        deck_section = soup.find('div', id=section_id)

        # Verificar si se encontró la sección
        if deck_section is None:
            print(f"No se encontró la sección de cartas del {section_name}.")
        else:
            # Recorrer cada carta en la sección del mazo
            for card in deck_section.find_all('a', class_='ygodeckcard'):
                # Buscar la imagen dentro del enlace
                img_tag = card.find('img', class_='lazy')
                if img_tag and 'data-cardname' in img_tag.attrs:
                    card_name = img_tag['data-cardname']
                    deck_data[section_name].append(card_name)
                else:
                    print(f"data-cardname no encontrado en: {img_tag}")

    # Crear un DataFrame con la información de las cartas
    deck_df = pd.DataFrame([
        {'Section': section, 'Card Name': card_name}
        for section, card_names in deck_data.items()
        for card_name in card_names
    ])

    # Obtener información adicional del mazo
    deck_name = soup.find('h1', class_='mt-5 text-break').text.strip()
    tournament_info = soup.find_all('span', class_='deck-metadata-child')

    # Extraer lugar, nombre del torneo y fecha
    place = tournament_info[0].find('b').text.strip()
    tournament_name = tournament_info[0].find('a').text.strip()
    date = tournament_info[2].text.strip()

    # Añadir la información adicional al DataFrame
    deck_df['Deck Name'] = deck_name
    deck_df['Place'] = place
    deck_df['Tournament Name'] = tournament_name
    deck_df['Date'] = date

    return deck_df

# Iterar sobre cada URL y obtener los datos del mazo
for index, row in urls_df.iterrows():
    base_url = "https://ygoprodeck.com"
    deck_url = row['URL del Deck']
    # Asegurarse de que la URL del deck no contenga una URL completa ya
    if deck_url.startswith("http"):
        full_url = deck_url
    else:
        full_url = base_url + deck_url  # Corregir la formación de la URL
    print(f"Procesando {full_url}")
    try:
        deck_df = obtener_datos_mazo(full_url)
        # Añadir las columnas originales del archivo Excel a cada DataFrame de mazo
        deck_df['Fecha'] = row['Fecha']
        deck_df['Nombre del Torneo'] = row['Nombre del Torneo']
        deck_df['URL del Torneo'] = row['URL del Torneo']
        deck_df['Jugadores'] = row['Jugadores']
        deck_df['Ganador'] = row['Ganador']
        all_decks_data.append(deck_df)
    except Exception as e:
        print(f"Error al procesar {full_url}: {e}")

# Concatenar todos los DataFrames en uno solo
final_df = pd.concat(all_decks_data, ignore_index=True)

# Guardar el DataFrame en un archivo Excel
excel_filename = 'cartas.xlsx'
final_df.to_excel(excel_filename, index=False)

print(f"Los datos de todos los mazos han sido guardados en el archivo '{excel_filename}'.")
