import os
from pathlib import Path
from google.cloud import firestore


# ─────────────────────────────────────────────
# PATH CONFIGURATION
PROJECT_ROOT_DIR = Path(__file__).resolve().parents[3] 
JSON_AUTH_PATH = PROJECT_ROOT_DIR / "app" / "backend" / "credentials" / "airline-chatbot-project-cbba19ed7161.json"

# ─────────────────────────────────────────────
# AUTHENTICATION SETUP (Set path to your downloaded JSON key)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = JSON_AUTH_PATH

# ─────────────────────────────────────────────
# FIRESTORE CLIENT INITIALIZATION
database = firestore.Client()