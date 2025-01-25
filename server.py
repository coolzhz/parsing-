from flask import Flask, jsonify, send_file, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import json
import os

app = Flask(__name__)

# Настройки для Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # Запуск в фоновом режиме
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Путь к ChromeDriver
CHROME_DRIVER_PATH = '/usr/local/bin/chromedriver'  # Путь на Render

# Папка для сохранения JSON-файлов
JSON_FOLDER = 'leagues_data'
if not os.path.exists(JSON_FOLDER):
    os.makedirs(JSON_FOLDER)

# Функция для сохранения данных в JSON
def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Данные сохранены в файл {filename}")

# Функция для получения списка лиг
def get_leagues():
    # Инициализация драйвера
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get('https://www.livescore.com/en/')

    # Ждем загрузки страницы
    time.sleep(5)  # Увеличьте время, если данные загружаются медленно

    # Получаем HTML-код страницы
    html = driver.page_source
    driver.quit()

    # Парсим данные
    soup = BeautifulSoup(html, 'html.parser')
    leagues = []

    # Пример поиска лиг (классы могут отличаться)
    league_elements = soup.find_all('div', class_='leagueTable')  # Уточните классы
    for league in league_elements:
        league_name = league.find('div', class_='leagueName').text.strip()
        leagues.append(league_name)

    return leagues

# Функция для парсинга данных с LiveScore
def parse_livescore(league_name):
    # Инициализация драйвера
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get('https://www.livescore.com/en/')

    # Ждем загрузки страницы
    time.sleep(5)  # Увеличьте время, если данные загружаются медленно

    # Получаем HTML-код страницы
    html = driver.page_source
    driver.quit()

    # Парсим данные
    soup = BeautifulSoup(html, 'html.parser')
    data = []

    # Пример поиска лиг и матчей (классы могут отличаться)
    league_elements = soup.find_all('div', class_='leagueTable')  # Уточните классы
    for league in league_elements:
        current_league_name = league.find('div', class_='leagueName').text.strip()
        if current_league_name == league_name:
            match_rows = league.find_all('div', class_='matchRow')  # Уточните классы
            for row in match_rows:
                team_home = row.find('div', class_='teamHome').text.strip()
                team_away = row.find('div', class_='teamAway').text.strip()
                score_full = row.find('div', class_='scoreFull').text.strip()  # Общий счёт
                score_half = row.find('div', class_='scoreHalf').text.strip()  # Счёт по таймам

                # Разделяем счёт по таймам (пример: "1-0 (0-0)")
                if '(' in score_half:
                    first_half, second_half = score_half.split('(')
                    first_half = first_half.strip()
                    second_half = second_half.replace(')', '').strip()
                else:
                    first_half = second_half = "N/A"

                data.append({
                    'team_home': team_home,
                    'team_away': team_away,
                    'score_full': score_full,
                    'score_first_half': first_half,
                    'score_second_half': second_half
                })

            # Сохраняем данные лиги в JSON-файл
            filename = os.path.join(JSON_FOLDER, f"{league_name}.json".replace('/', '_'))  # Заменяем слэши в названии
            save_to_json(data, filename)

            return data

    return []

# Маршрут для получения списка лиг
@app.route('/get-leagues', methods=['GET'])
def get_leagues_route():
    leagues = get_leagues()
    return jsonify(leagues)

# Маршрут для парсинга данных выбранной лиги
@app.route('/parse-league', methods=['POST'])
def parse_league():
    league_name = request.json.get('league_name')
    if not league_name:
        return jsonify({"error": "League name is required"}), 400

    data = parse_livescore(league_name)
    return jsonify(data)

# Маршрут для скачивания JSON-файла по названию лиги
@app.route('/download-json/<league_name>', methods=['GET'])
def download_json(league_name):
    filename = os.path.join(JSON_FOLDER, f"{league_name}.json")
    if os.path.exists(filename):
        return send_file(filename, as_attachment=True)
    else:
        return jsonify({"error": "File not found"}), 404

# Запуск сервера
if __name__ == '__main__':
    app.run(debug=True)
