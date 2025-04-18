import os
from dotenv import load_dotenv

load_dotenv(".env")

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")