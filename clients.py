# clients.py

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# OpenAI() will pick up OPENAI_API_KEY from environment
client = OpenAI()