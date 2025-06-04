import os
from datetime import datetime
from typing import Dict, Any
import json
from google.cloud import firestore

# ─────────────────────────────────────────────

# PATH CONFIGURATION
PROJECT_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
JSON_AUTH_PATH = os.path.join(PROJECT_ROOT_DIR, "app", "backend", "credentials", "airline-chatbot-project-cbba19ed7161.json")

# AUTHENTICATION SETUP (Set path to your downloaded JSON key)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = JSON_AUTH_PATH

# ─────────────────────────────────────────────
# FIRESTORE CLIENT INITIALIZATION
db = firestore.Client()
SESSIONS_COLLECTION = "sessions"  # Firestore collection name

def load_or_create_session(session_id: str) -> Dict[str, Any]:
    """
    Retrieves an existing session by ID or creates a new one if it doesn't exist.
    """
    doc_ref = db.collection(SESSIONS_COLLECTION).document(session_id)
    doc = doc_ref.get()

    if doc.exists:
        return doc.to_dict()

    # Create new session
    session_data = {
        "creation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "session_id": session_id,
        "conversation_history": [],
    }
    doc_ref.set(session_data)
    return session_data



def save_session(session_data: Dict[str, Any]) -> None:
    """
    Saves session data to Firestore.
    """
    session_id = session_data.get("session_id")
    if not session_id:
        raise ValueError("Session data must include a 'session_id' key.")

    doc_ref = db.collection(SESSIONS_COLLECTION).document(session_id)
    doc_ref.set(session_data)
