import requests
from bs4 import BeautifulSoup
import json

# URL de la Wikipedia del Premio Cervantes
url = "https://es.wikipedia.org/wiki/Premio_Cervantes"

# Obtener el HTML
res = requests.get(url)
res.raise_for_status()

# Parsear HTML
soup = BeautifulSoup(res.text, "html.parser")

# Encontrar todas las tablas con clase 'wikitable'
tablas = soup.find_all("table", class_="wikitable")

# Buscar la tabla correcta (la que tenga al menos 40 filas)
tabla_premiados = None
for tabla in tablas:
    filas = tabla.find_all("tr")
    if len(filas) > 40:
        tabla_premiados = tabla
        break

if not tabla_premiados:
    print("No se encontró la tabla adecuada.")
    exit()

# Extraer datos
resultados = []

for fila in tabla_premiados.find_all("tr")[1:]:  # Omitir encabezado
    celdas = fila.find_all("td")
    if len(celdas) < 3:
        continue  # Saltar filas incompletas o notas

    try:
        year = int(celdas[0].text.strip())
    except ValueError:
        continue

    name = celdas[1].text.strip()
    nationality = celdas[2].text.strip()

    resultados.append({
        "year": year,
        "name": name,
        "nationality": nationality
    })

# Guardar como JSON
with open("premios_cervantes.json", "w", encoding="utf-8") as f:
    json.dump(resultados, f, ensure_ascii=False, indent=2)

print(f"Guardados {len(resultados)} registros.")
