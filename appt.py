from flask import Flask, request
import requests

app = Flask(__name__)

TELEGRAM_TOKEN = '8044022972:AAHAlilUYiWuTu1XK9dLj0mTe6kybJBTal4'  
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

DEEPSEEK_API_KEY = 'sk-e101d52f3c8b421686dda4b0a1a665ca' 
DEEPSEEK_URL = 'https://api.deepseek.com/v1/chat/completions'

@app.route('/', methods=['GET'])
def home():
    return 'Bot de Telegram + IA activo ✅'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Datos recibidos:", data)  # 🛑 Aquí imprimimos todo lo que recibe el webhook

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        user_message = data["message"]["text"]

        # Obtener nombre del usuario
        user_first_name = data["message"]["from"].get("first_name", "usuario")
        user_last_name = data["message"]["from"].get("last_name", "")
        full_name = f"{user_first_name} {user_last_name}".strip()

        # Preparar el mensaje para DeepSeek
        full_prompt = (
            "Eres Cecy, una amiga cercana, empática y confiable 🧡. "
            "Ayudas a personas que enfrentan problemas como drogadicción 🚭, embarazos no deseados 🤰, "
            "salud mental 🧠 y bullying 😔. "
            "Responde de manera cálida, positiva, amigable y siempre solidaria. "
            "Usa un lenguaje sencillo y afectuoso, incluye emojis para transmitir cercanía. "
            "No uses tecnicismos, ni juzgues a nadie. "
            "Firma cada mensaje como Cecy 🌸 al final de tu respuesta."
        )

        # Pedir respuesta a DeepSeek
        response = ask_deepseek(user_message, full_prompt)
        print("Respuesta de DeepSeek:", response)  # 🛑 Verificamos la respuesta de DeepSeek

        # Enviar la respuesta al usuario
        send_message(chat_id, response)

    return 'ok', 200

def ask_deepseek(user_message, full_prompt):
    headers = {
        'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": full_prompt},
            {"role": "user", "content": user_message}
        ],
    }
    r = requests.post(DEEPSEEK_URL, json=payload, headers=headers)
    if r.status_code == 200:
        response_data = r.json()
        return response_data['choices'][0]['message']['content']
    else:
        print("Error al consultar :", r.text)  # 🛑 Imprimimos el error si ocurre
        return "Lo siento, hubo un error al procesar tu mensaje. 😥"

def send_message(chat_id, text):
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    r = requests.post(TELEGRAM_API_URL, json=payload)
    print("Respuesta de Telegram:", r.text)  # 🛑 Imprimimos qué respondió Telegram

if __name__ == '__main__':
    app.run(port=5000)
    
