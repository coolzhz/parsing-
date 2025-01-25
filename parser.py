import requests
from bs4 import BeautifulSoup
import json
import os

# Парсинг данных
url = "https://www.livescore.com/en/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Папка для сохранения JSON-файлов
DATA_FOLDER = "leagues_data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# Пример поиска лиг и матчей (классы могут отличаться)
leagues = soup.find_all("div", class_="league")  # Уточните классы
for league in leagues:
    league_name = league.find("div", class_="league-name").text.strip()
    matches = []
    match_rows = league.find_all("div", class_="match")  # Уточните классы
    for row in match_rows:
        team_home = row.find("div", class_="team-home").text.strip()
        team_away = row.find("div", class_="team-away").text.strip()
        score_full = row.find("div", class_="score-full").text.strip()
        score_half = row.find("div", class_="score-half").text.strip()
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
