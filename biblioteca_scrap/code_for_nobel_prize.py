import requests
from bs4 import BeautifulSoup
import json

URL = "https://en.wikipedia.org/wiki/List_of_Nobel_laureates_in_Literature"

resp = requests.get(URL)
resp.raise_for_status()

soup = BeautifulSoup(resp.text, "html.parser")

tabla = soup.find("table", {"class": "wikitable"})
result = []

for fila in tabla.find_all("tr")[1:]:
    celdas = fila.find_all(["th", "td"])
    if len(celdas) < 5:
        continue

    try:
        year = int(celdas[0].get_text(strip=True))
    except ValueError:
        continue

    if 1994 <= year <= 2024:
        name = celdas[1].get_text(strip=True).replace("\xa0", " ")
        country = celdas[3].get_text(strip=True).replace("\xa0", " ")
        language = celdas[4].get_text(strip=True).replace("\xa0", " ")

        result.append({
            "year": year,
            "name": name,
            "nationality": country,
            "language": language
        })

with open("nobel_literature_1994_2024.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)