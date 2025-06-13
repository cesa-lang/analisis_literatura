import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Configuración de Selenium (modo headless)
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

# Cargar la página de bestsellers
url = "https://www.amazon.com/gp/bestsellers/2024/books"
driver.get(url)
time.sleep(5)
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

# JSON con los libros incompletos
incompletos = [
    {"Autor": "Robert Greene", "Precio": "N/A", "Estrellas": 4.7},
    {"Autor": "Sarah J. Maas", "Precio": "N/A", "Estrellas": 4.6},
    {"Autor": "Rebecca Yarros", "Precio": "US$5.02", "Estrellas": 4.7},
    {"Autor": "Dav Pilkey", "Precio": "US$11.90", "Estrellas": 4.8},
    {"Autor": "Freida McFadden", "Precio": "US$1.55", "Estrellas": 4.4},
    {"Autor": "Rebecca Yarros", "Precio": "US$15.23", "Estrellas": 4.8},
    {"Autor": "Melania Trump", "Precio": "N/A", "Estrellas": 4.6},
    {"Autor": "Bessel van der Kolk M.D.", "Precio": "N/A", "Estrellas": 4.8},
    {"Autor": "Colleen Hoover", "Precio": "US$1.85", "Estrellas": 4.5},
    {"Autor": "Emma Greene", "Precio": "N/A", "Estrellas": 4.7},
    {"Autor": "Jeff Kinney", "Precio": "US$2.46", "Estrellas": 4.7},
    {"Autor": "Kristin Hannah", "Precio": "N/A", "Estrellas": 4.7},
    {"Autor": "Freida McFadden", "Precio": "N/A", "Estrellas": 4.2},
    {"Autor": "Coco Wyo", "Precio": "N/A", "Estrellas": 4.8},
    {"Autor": "Morgan Housel", "Precio": "US$9.25", "Estrellas": 4.7},
    {"Autor": "Amelia Hepworth", "Precio": "N/A", "Estrellas": 4.9},
    {"Autor": "Sarah J. Maas", "Precio": "N/A", "Estrellas": 4.8},
]

# Extraer libros de la página
libros = []
for card in soup.select(".zg-grid-general-faceout"):
    title = card.select_one(".p13n-sc-truncate") or card.select_one("img")
    autor = card.select_one(".a-row.a-size-small")
    precio = card.select_one(".p13n-sc-price")
    estrellas = card.select_one(".a-icon-alt")
    ratings = card.select_one(".a-size-small .a-link-normal")

    libros.append({
        "Título": title.get_text(strip=True) if title else None,
        "Autor": autor.get_text(strip=True) if autor else None,
        "Precio": precio.get_text(strip=True) if precio else None,
        "Estrellas": float(estrellas.get_text().split()[0]) if estrellas else None,
        "Número de Calificaciones": ratings.get_text(strip=True) if ratings else None,
        "Tipo de Lista": None  # No está presente en la página de forma directa
    })

# Completar JSON con coincidencias por autor + precio/estrellas
result = []
for rec in incompletos:
    match = next((b for b in libros if b["Autor"] == rec["Autor"]
                  and (rec["Precio"] == "N/A" or b["Precio"] == rec["Precio"])
                  and (rec["Estrellas"] == b["Estrellas"])), None)
    if match:
        rec.update({
            "Título": match["Título"],
            "Precio": match["Precio"],
            "Número de Calificaciones": match["Número de Calificaciones"],
            "Tipo de Lista": match["Tipo de Lista"]
        })
    result.append(rec)

# Guardar en JSON
with open("bestsellers_amazon_2024_completos.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Completados {sum(1 for x in result if x['Título'])} de {len(result)} registros.")