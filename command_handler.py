import re
import weather


def handle_commands(msg: str):
    if msg == "/forecast5":
        if msg == "/city":
            return weather.forecast(msg)
    else:
        return msg


handle_commands("/forecast5")
