from flask import Flask, request
from openai import OpenAI
import requests

app = Flask(__name__)

TELEGRAM_TOKEN = '8044022972:AAHAlilUYiWuTu1XK9dLj0mTe6kybJBTal4'
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

DEEPSEEK_API_KEY = 'sk-e0296482ea0b4343a23e1a796a6683f8'
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com/v1"
)

@app.route('/', methods=['GET'])
def home():
    return 'Bot de Telegram + IA activo ✅'

@app.route('/webhook', methods=['POST'])
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
        try:
            response = open.ChatCompletion.create(
                model="gpt-3.5-turbo",  # DeepSeek utiliza GPT-3.5 o GPT-4
                messages=[
                    {{"role": "system", "content": (
                        "Eres Cecy, una amiga cercana, empática y confiable 🧡. "
                        "Siempre respondes de manera amable, con un tono cálido y positivo. "
                        "Te gusta apoyar, animar, aconsejar de forma sencilla y con cariño. "
                         "Nunca suenas como un robot; eres como una amiga que escucha y conversa."
                        )}
                        },
                    {"role": "user", "content": user_message}
                        ]   
            )
            bot_response = response['choices'][0]['message']['content']
        except Exception as e:
            print("Error al consultar DeepSeek:", e)
            bot_response = (
            "☕ ¡Hola, soy Cecy! Parece que estoy tomándome un pequeño descanso técnico. "
            "Estoy trabajando para estar de vuelta muy pronto. 🛠️ ¡No te vayas lejos! 🧡"
            )

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
    import requests
import json

# URL de la API de DeepSeek
url = "https://api.deepseek.com/v1"  # Reemplaza con la URL correcta si cambia

# Tu clave API
api_key = "sk-e0296482ea0b4343a23e1a796a6683f8"  

# Los encabezados de la solicitud, incluyendo la autorización con tu API Key
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# El cuerpo de la solicitud (la consulta que quieres enviar)
data = {
    "query": "¿Qué es la inteligencia artificial?",  # Aquí puedes poner la pregunta o texto que deseas procesar
    "model": "deepseek-chat"  # Ajusta esto si utilizas un modelo diferente
}

# Hacer la solicitud POST a la API
response = requests.post(url, headers=headers, json=data)

# Comprobar si la solicitud fue exitosa
if response.status_code == 200:
    # Si la respuesta es exitosa, muestra los resultados
    print("Respuesta de la API:", json.dumps(response.json(), indent=4))
else:
    # Si hubo un error, muestra el código de estado y el error
    print(f"Error: {response.status_code}, {response.text}")

