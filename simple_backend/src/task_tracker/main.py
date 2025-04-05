import requests
from flask import Flask, jsonify, request

app = Flask(Даниил)


API_KEY = '$2a$10$kowFjWD5dHKedIYMb6MbPe4DJ.7LmQI3aBxv3FAOFFdB8XGxe9ZsG'
BIN_ID = '67eeb21c8561e97a50f81d9f'  

# Заголовки для аутентификации
headers = {
    'Content-Type': 'application/json',
    'secret-key': API_KEY
}

@app.route('/data', methods=['GET'])
def get_data():
    response = requests.get(f'https://api.jsonbin.io/v3/b/{BIN_ID}', headers=headers)
    return jsonify(response.json()), response.status_code

@app.route('/data', methods=['POST'])
def update_data():
    data = request.json  
    response = requests.put(f'https://api.jsonbin.io/v3/b/{BIN_ID}', json=data, headers=headers)
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
