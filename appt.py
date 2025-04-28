from flask import Flask, request
import requests
import json
app = Flask(__name__)

TELEGRAM_TOKEN = '8044022972:AAHAlilUYiWuTu1XK9dLj0mTe6kybJBTal4'
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

DEEPSEEK_API_KEY = 'sk-e0296482ea0b4343a23e1a796a6683f8'
DEEPSEEK_API_URL = 'https://api.deepseek.com'  # URL del endpoint de DeepSeek

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
        user_first_name = data["message"]["from"].get("first_name", "amigo/a")
        user_last_name = data["message"]["from"].get("last_name", "")
        full_name = f"{user_first_name} {user_last_name}".strip()

        # Definir la personalidad de Cecy en el mensaje a DeepSeek
        system_message = (
            "Eres Cecy, una amiga cercana, empática y confiable 🧡. "
            "Siempre respondes de manera amable, con un tono cálido y positivo. "
            "Te gusta apoyar, animar, aconsejar de forma sencilla y con cariño. "
            "Nunca suenas como un robot; eres como una amiga que escucha y conversa. "
            "Tu estilo de conversación es cercano, optimista y siempre buscas alegrar a los demás. "
            "A veces haces preguntas para que la conversación siga fluyendo y nunca eres brusca. "
            "Usas emojis y expresiones para que la charla sea más cálida y natural. 😊"
        )

        # Preparar la consulta para DeepSeek
        try:
            payload = {
                "query": user_message,  # El mensaje del usuario
                "model": "deepseek-chat",  # Ajusta si necesitas un modelo diferente
            }

            headers = {
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            }

            # Enviar la consulta a la API de DeepSeek
            response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
            response.raise_for_status()

            # Obtener la respuesta de DeepSeek
            response_data = response.json()
            bot_response = response_data.get("response", "Lo siento, no pude procesar tu solicitud en este momento. 😕")

        except requests.exceptions.RequestException as e:
            print("Error al consultar DeepSeek:", e)
            bot_response = (
                "¡Ups! Parece que hubo un problema, pero no te preocupes, ¡estoy aquí para ayudarte! 🧡 "
                "Si quieres, intenta de nuevo o cuéntame más. 😊"
            )

        # Personalizar la respuesta con el nombre del usuario
        bot_response = f"¡Hola, {user_first_name}! 😊\n\n{bot_response}\n\n¿Hay algo más en lo que pueda ayudarte? 💬"

        # Enviar la respuesta al usuario en Telegram
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
