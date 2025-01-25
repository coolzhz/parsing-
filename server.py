from flask import Flask, jsonify, send_file
import os
import json

app = Flask(__name__)

# Папка с JSON-файлами
DATA_FOLDER = "leagues_data"

# Маршрут для получения списка лиг
@app.route('/leagues', methods=['GET'])
def get_leagues():
    leagues = [f.replace('.json', '') for f in os.listdir(DATA_FOLDER) if f.endswith('.json')]
    return jsonify(leagues)

# Маршрут для получения матчей выбранной лиги
@app.route('/leagues/<league>', methods=['GET'])
def get_matches(league):
    filename = os.path.join(DATA_FOLDER, f"{league}.json")
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            matches = json.load(f)
        return jsonify(matches)
    else:
        return jsonify({"error": "League not found"}), 404

# Запуск сервера
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
