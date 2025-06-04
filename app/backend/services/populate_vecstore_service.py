import os
from dotenv import load_dotenv
from openai import OpenAI
from chromadb import PersistentClient
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from app.backend.utils.utils import get_config_value

# ─────────────────────────────────────────────
# PATH CONFIGURATION
PROJECT_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
KNOWLEDGE_FILE_PATH = os.path.join(PROJECT_ROOT_DIR, "data", "documents", "knowledge.txt")
VECTOR_STORE_PATH = os.path.join(PROJECT_ROOT_DIR, "data", "vectorstore")
DOTENV_PATH = os.path.join(PROJECT_ROOT_DIR, ".env")

# ─────────────────────────────────────────────
# CLIENT INITIALIZATION
load_dotenv(DOTENV_PATH)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY is not set in the .env file.")

openai_client = OpenAI(api_key=OPENAI_API_KEY)
chroma_client = PersistentClient(path=VECTOR_STORE_PATH)
embedding_fn = OpenAIEmbeddingFunction(api_key=OPENAI_API_KEY)
collection = chroma_client.get_or_create_collection(name="knowledge", embedding_function=embedding_fn)

# ─────────────────────────────────────────────
# KNOWLEDGE BASE INGESTION

def load_knowledge_chunks(file_path: str, delimiter: str = "----------") -> list[str]:
    """Loads and splits the knowledge base into clean chunks."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Knowledge base file not found at {file_path}")

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    chunks = [chunk.strip() for chunk in content.split(delimiter) if chunk.strip()]
    if not chunks:
        raise ValueError("Knowledge base is empty or not correctly formatted.")

    return chunks

def clear_vectorstore() -> None:
    """Clears existing documents from the vector store collection."""
    existing_ids = collection.get().get("ids", [])
    if existing_ids:
        collection.delete(ids=existing_ids)
        print(f"🧹 Deleted {len(existing_ids)} existing documents from the collection.")
    else:
        print("✅ Collection is already empty.")

def populate_vectorstore(chunks: list[str]) -> None:
    """Adds new knowledge chunks to the vector store."""
    for idx, chunk in enumerate(chunks):
        collection.add(ids=[f"chunk-{idx}"], documents=[chunk])
    print(f"✅ Successfully added {len(chunks)} chunks to the vector store.")

if __name__ == "__main__":
    try:
        knowledge_chunks = load_knowledge_chunks(KNOWLEDGE_FILE_PATH)
        clear_vectorstore()
        populate_vectorstore(knowledge_chunks)
    except (FileNotFoundError, ValueError, EnvironmentError) as e:
        print(f"⚠️ Error: {str(e)}")
