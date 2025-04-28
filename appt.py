from flask import Flask, request
import openai
import requests

app = Flask(__name__)

TELEGRAM_TOKEN = '8044022972:AAHAlilUYiWuTu1XK9dLj0mTe6kybJBTal4'
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

DEEPSEEK_API_KEY = 'sk-e0296482ea0b4343a23e1a796a6683f8'
openai.api_key = DEEPSEEK_API_KEY  # Usamos la API Key de DeepSeek (OpenAI en este caso)

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

        # Obtener nombre del usuario
        user_first_name = data["message"]["from"].get("first_name", "usuario")
        user_last_name = data["message"]["from"].get("last_name", "")
        full_name = f"{user_first_name} {user_last_name}".strip()

        # Preparar el mensaje para DeepSeek (usando OpenAI)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # DeepSeek utiliza GPT-3.5 o GPT-4
            messages=[
                {"role": "system", "content": "Eres Cecy, una amiga cercana, empática y confiable 🧡."},
                {"role": "user", "content": user_message}
            ]
        )

        # Obtener la respuesta de OpenAI (DeepSeek)
        bot_response = response['choices'][0]['message']['content']
        print("Respuesta de DeepSeek:", bot_response)

        # Enviar la respuesta a Telegram
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
    