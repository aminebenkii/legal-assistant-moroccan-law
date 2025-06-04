import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# ─────────────────────────────────────────────
# PATH CONFIGURATION
PROJECT_ROOT_DIR = Path(__file__).resolve().parents[2]
DOTENV_PATH = PROJECT_ROOT_DIR / ".env"

# ─────────────────────────────────────────────
# ENV VARS LOADING
load_dotenv(DOTENV_PATH)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Missing OPENAI_API_KEY in .env")

# ─────────────────────────────────────────────
# CLIENT INITIALIZATION
openai_client = OpenAI(api_key=OPENAI_API_KEY)
