import os, datetime
from dotenv import load_dotenv
from openai import OpenAI
from chromadb import PersistentClient
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from app.backend.utils.utils import get_config_value

# ─────────────────────────────────────────────
# PATH CONFIGURATION
PROJECT_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
VECTOR_STORE_PATH = os.path.join(PROJECT_ROOT_DIR, "data", "vectorstore")
DOTENV_PATH = os.path.join(PROJECT_ROOT_DIR, ".env")

# ─────────────────────────────────────────────
# API & CLIENT INITIALIZATION
load_dotenv(DOTENV_PATH)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

chroma_client = PersistentClient(path=VECTOR_STORE_PATH)
embedding_fn = OpenAIEmbeddingFunction(api_key=OPENAI_API_KEY)
collection = chroma_client.get_or_create_collection(name="knowledge", embedding_function=embedding_fn)

# ─────────────────────────────────────────────
# FUNCTION DEFINITIONS

def build_contextual_query(conversation: list[str]) -> str:
    """Builds a retrieval query using the last 3 conversation turns."""

    num_history_turns = int(get_config_value("NUM_RETRIEVAL_TURNS")) if get_config_value("NUM_RETRIEVAL_TURNS") else 3
    recent_messages = conversation[-num_history_turns:]
    return "\n".join(msg.get("content", "") for msg in recent_messages)


def retrieve_context_chunks(query: str) -> str:
    """Retrieves top context chunks from the vector store based on the query."""

    num_chunks = int(get_config_value("NUM_CONTEXT_CHUNKS")) if get_config_value("NUM_CONTEXT_CHUNKS") else 5
    results = collection.query(query_texts=[query], n_results=num_chunks)
    documents = results.get("documents", [[]])[0] if results else []
    return "\n\n".join(documents)

