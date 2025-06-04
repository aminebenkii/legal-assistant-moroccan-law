import os
from pathlib import Path
from dotenv import load_dotenv
from chromadb import PersistentClient
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

# ─────────────────────────────────────────────
# PATH CONFIGURATION
PROJECT_ROOT_DIR = Path(__file__).resolve().parents[3] 
VECTOR_STORE_PATH =  PROJECT_ROOT_DIR / "app" / "backend" / "vectorstore"
DOTENV_PATH = PROJECT_ROOT_DIR / ".env"

# ─────────────────────────────────────────────
# ENV VARS LOADING
load_dotenv(DOTENV_PATH)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ─────────────────────────────────────────────
# CLIENT INITIALIZATION
chroma_client = PersistentClient(path=VECTOR_STORE_PATH)
embedding_fn = OpenAIEmbeddingFunction(api_key=OPENAI_API_KEY)
collection = chroma_client.get_or_create_collection(name="knowledge", embedding_function=embedding_fn)

