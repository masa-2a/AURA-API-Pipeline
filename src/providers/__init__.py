from pathlib import Path
from dotenv import load_dotenv
import os

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(env_path)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMENI_API_KEY = os.getenv("GEMINI_API_KEY")