import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = 'english'
    DEBUG = os.getenv('DEBUG', 'False') == 'True'


