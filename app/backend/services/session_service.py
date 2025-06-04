from datetime import datetime
from typing import Dict, Any
from app.backend.core.firestore_client import database as db


# ─────────────────────────────────────────────
# CONSTANTS
SESSIONS_COLLECTION = "sessions"  

# ─────────────────────────────────────────────
# FUNCTION DEFINITIONS

def load_or_create_session(session_id):
    """Retrieves an existing session by ID or creates a new one if it doesn't exist."""

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
    """Saves session data to Firestore."""

    session_id = session_data.get("session_id")
    if not session_id:
        raise ValueError("Session data must include a 'session_id' key.")

    doc_ref = db.collection(SESSIONS_COLLECTION).document(session_id)
    doc_ref.set(session_data)
