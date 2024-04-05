import os
from dotenv import load_dotenv


ENV_DIR = os.path.join(os.getcwd(), '.env')

load_dotenv(ENV_DIR)

HF_HUB_TOKEN = os.getenv('HUGGING_FACE_HUB_READ_TOKE')
