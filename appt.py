

from flask import Flask, request
import requests

app = Flask(__name__)

TELEGRAM_TOKEN = '80444022972'
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

DEEPSEEK_API_KEY = 'sk-e101d52f3c8b421686dda4b0a1a665ca'
DEEPSEEK_URL = 'https://api.deepseek.com/v1/chat/completions'

@app.route('/', methods=['GET'])
def home():
    return 'Bot de Telegram + DeepSeek activo ✅'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        user_message = data["message"]["text"]
        
        # Obtener el nombre del usuario
        user_first_name = data["message"]["from"].get("first_name", "usuario")
        user_last_name = data["message"]["from"].get("last_name", "")
        full_name = f"{user_first_name} {user_last_name}".strip()

        # Pedir respuesta a DeepSeek
        response = ask_deepseek(user_message, full_name)
        
        # Enviar la respuesta al usuario
        send_message(chat_id, response)

    return 'ok', 200

def ask_deepseek(user_message, user_name):
    headers = {
        'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": f"{user_name} dice: {user_message}"}],
    }
    r = requests.post(DEEPSEEK_URL, json=payload, headers=headers)
    if r.status_code == 200:
        response_data = r.json()
        return response_data['choices'][0]['message']['content']
    else:
        return "Lo siento, hubo un error preguntando a DeepSeek."

def send_message(chat_id, text):
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    requests.post(TELEGRAM_API_URL, json=payload)

if __name__ == '__main__':
    app.run(port=5000)
