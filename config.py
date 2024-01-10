import os

from dotenv import load_dotenv

load_dotenv()

TG_TOKEN = os.getenv('TG_TOKEN')
DATA_BASE = os.getenv('DATA_BASE')
MENU = os.getenv('MENU')
DATA_FOLDER = os.getenv('DATA_FOLDER')
