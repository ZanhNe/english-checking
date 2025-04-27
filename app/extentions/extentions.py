from flask_cors import CORS
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
import os

load_dotenv()

cors = CORS(resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
eleven_client = ElevenLabs(api_key=os.getenv('ELEVENLAB_API_KEY'))




