from flask import Flask, request
from openai import OpenAI
import requests

app = Flask(__name__)

TELEGRAM_TOKEN = '8044022972:AAHAlilUYiWuTu1XK9dLj0mTe6kybJBTal4'
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

DEEPSEEK_API_KEY = 'sk-e0296482ea0b4343a23e1a796a6683f8'
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

@app.route('/', methods=['GET'])
def home():
    return 'Bot de Telegram + IA activo ✅'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Datos recibidos:", data)

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        user_message = data["message"]["text"]

        # Preparar el mensaje para DeepSeek
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "Eres Cecy, una amiga cercana, empática y confiable 🧡."},
                {"role": "user", "content": user_message}
            ]
        )

        bot_response = response.choices[0].message.content
        print("Respuesta de DeepSeek:", bot_response)

        send_message(chat_id, bot_response)

    return 'ok', 200

def send_message(chat_id, text):
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    r = requests.post(TELEGRAM_API_URL, json=payload)
    print("Respuesta de Telegram:", r.text)

if __name__ == '__main__':
    app.run(port=5000)
