from flask import Flask, request, Response
import requests
from dotenv import load_dotenv
import os
import json
from langchain_community.llms import Ollama

llm = Ollama(model="llama2")
load_dotenv()


TOKEN = os.getenv('HTTP_API_TOKEN')
BASE_URL = f"https://api.telegram.org/bot{TOKEN}/"
ngrok_url = os.getenv("NGROK_URL")
telegram_webhook = BASE_URL + "setWebhook?" + "url=" + ngrok_url
app = Flask(__name__)


def parse_message(message: dict) -> tuple:
    chat_id = message.get('message', {}).get('chat', {}).get('id')
    text = message.get('message', {}).get('text')
    if chat_id is None or text is None:
        print("Error: Missing data in message")
        return (None, None)
    return (chat_id, str(text))


def write_json(data: dict) -> None:
    with open('telegram_request.json', "w") as file:
        json.dump(data, file)


def send_message(chat_id: int, text: str = "...") -> bool:
    url = BASE_URL + 'sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    try:
        respond = requests.post(url, json=payload)
        respond.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")
        return False
    return True


@app.route('/', methods=['POST', 'GET'])
def bot():
    if request.method == 'POST':
        message = request.get_json()
        chat_id, text = parse_message(message)
        write_json(message)
        msg = llm.invoke(text)
        send_message(chat_id, text)
        return Response('OK', status=200)
    else:
        return Response('Internal Server Error', status=500)


@app.route('/setwebhook/')
def setwebhook():
    return "OK" if requests.get(telegram_webhook) else "FAIL"

# requests.get(telegram_webhook)


if __name__ == '__name__':
    app.run(debug=True)
