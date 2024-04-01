import requests
from dotenv import load_dotenv
import os
import json
from paibot import BASE_URL, TOKEN, write_json

set_command_url = f"https://api.telegram.org/bot{TOKEN}/setMyCommands?commands="
commands: dict[str, str] = [{
    "command": "forecast5",
    "description": "weather forcasting 5 days"
},
    {
    "command": "forecast10",
    "description": "weather forcasting 10 days"
}]

write_json(commands, filename='commands.js')

set_commands = str(json.dumps(commands))
set_commands = set_command_url + set_commands
response = requests.get(set_commands)
print(set_command_url)
print(set_commands)
print(response)
