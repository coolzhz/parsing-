from flask import Flask, jsonify, send_file, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
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
chrome_options.add_argument("--disable-dev-shm-usage")  # Уменьшает использование памяти

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
                    firs
