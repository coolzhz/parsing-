import requests
from bs4 import BeautifulSoup
import json
import os

# Папка для сохранения JSON-файлов
DATA_FOLDER = "leagues_data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# URL сайта для парсинга
url = "https://www.livescore.com/en/"

# Заголовки для имитации запроса от браузера
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Запрос к сайту
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Поиск лиг и матчей
leagues = soup.find_all("div", class_="league")  # Уточните классы
data = {}

for league in leagues:
    league_name = league.find("div", class_="league__name").text.strip()  # Уточните классы
    matches = []

    # Поиск матчей в лиге
    match_rows = league.find_all("div", class_="match")  # Уточните классы
    for row in match_rows:
        team_home = row.find("div", class_="team__home").text.strip()  # Уточните классы
        team_away = row.find("div", class_="team__away").text.strip()  # Уточните классы
        score_full = row.find("div", class_="score__full").text.strip()  # Уточните классы
        score_half = row.find("div", class_="score__half").text.strip()  # Уточните классы

        matches.append({
            "team_home": team_home,
            "team_away": team_away,
            "score_full": score_full,
            "score_half": score_half
        })

    # Сохранение данных лиги в отдельный JSON-файл
    filename = os.path.join(DATA_FOLDER, f"{league_name}.json".replace('/', '_'))  # Заменяем слэши в названии
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(matches, f, ensure_ascii=False, indent=4)

    data[league_name] = matches

print("Парсинг завершен. Данные сохранены в папку leagues_data/.")
