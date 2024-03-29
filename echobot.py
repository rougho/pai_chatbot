import os
import json
from dotenv import load_dotenv
import requests
import time

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


def get_updates(offset: int = None) -> dict:
    url = URL + "getUpdates"
    if offset:
        url += f"?offset={offset}"
    js = get_json(url)
    return js


def get_last_update_id(updates: dict) -> int:
    result = updates.get('result', [])
    update_ids = [int(item.get('update_id', 0)) for item in result if isinstance(
        item.get('update_id'), (int, list))]
    return max(update_ids) if update_ids else 0


print(get_last_update_id(get_updates()))


def echo_all(updates: dict) -> None:
    for update in updates.get('result', []):
        try:
            message = update.get('message', {})
            text = message.get('text')
            chat_id = message.get('chat', {}).get('id', 0)
            send_message(text, chat_id)
        except Exception as e:
            print(f"echo_all: {e}")


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


def echo_message():
    last_update_id = None

    while True:
        updates = get_updates(last_update_id)

        if len(updates.get('result', 0)) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    echo_message()
