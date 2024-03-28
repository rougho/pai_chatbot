import os
import json
import logging
from dotenv import load_dotenv
import requests

# load .env
load_dotenv()

TOKEN = os.getenv('HTTP_API_TOKEN')
URL = f"https://api.telegram.org/bot{TOKEN}/"


def get_url(url):
    """ Fetches the content of the provided URL and returns it as a decoded string.

    This function uses the `requests` library to make an HTTP GET request to the specified URL.
    If successful, it decodes the response content using UTF-8 encoding and returns the decoded string.

    Args:
        url (str): The URL to fetch content from.

    Returns:
        str: The decoded content of the URL, or None if an error occurs.

    """
    try:
        respone = requests.get(url)
        content = respone.content.decode('utf8')
        return content
    except requests.exceptions.RequestException as e:
        print("error: ", e)


def get_json(url):
    pass
