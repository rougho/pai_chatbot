from flask import Flask, request, Response
import requests
from dotenv import load_dotenv
import os
import json
import re
from langchain_community.llms import Ollama
import weather
llm = Ollama(model="llama2")
load_dotenv()


TOKEN: str = os.getenv('HTTP_API_TOKEN')
BASE_URL: str = f"https://api.telegram.org/bot{TOKEN}/"
ngrok_url: str = os.getenv("NGROK_URL")
telegram_webhook: str = f"{BASE_URL}setWebhook?url={ngrok_url}"


app: object = Flask(__name__)


def re_exp(message: str):
    pattern = r'/[a-zA-Z]{2-4}'
    ticker = re.findall(pattern, message)
    return ticker[0] if ticker else ''


def parse_message(message: dict[str, str]) -> tuple[str]:
    chat_id: str = message.get('message', {}).get('chat', {}).get('id')
    text: str = message.get('message', {}).get('text')
    if chat_id is None or text is None:
        print("Error: Missing data in message")
        return (None, None)
    return (chat_id, str(text))


def write_json(data: dict[str, str], filename: str = 'telegram_request.json') -> None:
    with open(filename, "w") as file:
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
        # msg = llm.invoke(text)
        if text == "/forecast5":
            send_message(chat_id, weather.get_forecast(52.52437, 13.41053))
        return Response('OK', status=200)
    else:
        return Response('Internal Server Error', status=500)


@app.route('/setwebhook')
def setwebhook():
    print(telegram_webhook)
    payload = {"url": ngrok_url}
    response = requests.post(telegram_webhook, json=payload)
    return response.json() if response.status_code == 200 else "FAIL"


if __name__ == '__name__':
    app.run(debug=True, port=5000)
