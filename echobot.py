import os
import json
from dotenv import load_dotenv
import requests

# load .env
load_dotenv()

TOKEN = os.getenv('HTTP_API_TOKEN')
URL = f"https://api.telegram.org/bot{TOKEN}/"


def get_url(url: str) -> str:
    try:
        respone = requests.get(url)
        # respone.raise_for_status()
        content = respone.content.decode('utf8')
        return content
    except requests.exceptions.RequestException as e:
        print(f"error: {e}")
        return None


def get_json(url: str) -> dict:
    content = get_url(url)
    js = json.loads(content)
    return js


def get_update() -> dict:
    url = URL + "getUpdates"
    js = get_json(url)
    return js


def get_last_chat(updates: dict) -> tuple:
    number_of_updates = len(updates['result'])
    last_update = number_of_updates - 1
    text = updates.get('result', [])[last_update].get(
        'message', {}).get('text', 0)
    chat_id = updates.get('result', [])[last_update].get(
        'message', {}).get('chat').get('id', 0)
    return (text, chat_id)


def send_message(text: str, chat_id: str) -> None:
    url = URL + f"sendMessage?text={text}&chat_id={chat_id}"
    get_url(url)


text, chat = get_last_chat(get_update())
print(chat, text)
send_message(text, chat)
