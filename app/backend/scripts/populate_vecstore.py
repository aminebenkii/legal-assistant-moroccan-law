import json
from pathlib import Path
from app.backend.core.chromadb_client import collection


# ─────────────────────────────────────────────
# PATH CONFIGURATION
PROJECT_ROOT_DIR = Path(__file__).resolve().parents[3]
KNOWLEDGE_FILE_PATH = PROJECT_ROOT_DIR / "data" / "processed" / "knowledge.txt"
VECTOR_STORE_PATH =  PROJECT_ROOT_DIR / "app" / "backend" / "vectorstore"


# ─────────────────────────────────────────────
# KNOWLEDGE BASE INGESTION


def extract_chunks_from_json_file(file_path, key: str = "content") -> list[str]:

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Expected a list of objects in the JSON file.")

    chunks = [item[key].strip() for item in data if key in item and isinstance(item[key], str)]

    if not chunks:
        raise ValueError(f"No valid '{key}' entries found in JSON.")

    return chunks


def split_text_file_into_chunks(file_path, delimiter = "----------"):
    
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    chunks = [chunk.strip() for chunk in content.split(delimiter) if chunk.strip()]
    if not chunks:
        raise ValueError("Knowledge base is empty or not correctly formatted.")

    return chunks


def clear_vectorstore():
    
    existing_ids = collection.get().get("ids", [])
    
    if existing_ids:
        collection.delete(ids=existing_ids)
        print(f"Deleted existing documents from the collection.")
    else:
        print("Collection already empty.")


def populate_vectorstore(chunks):
    
    for idx, chunk in enumerate(chunks):
        collection.add(ids=[f"chunk-{idx}"], documents=[chunk])

    print(f"Successfully added {len(chunks)} chunks to the vector store.")


if __name__ == "__main__":

    try:
        knowledge_chunks = split_text_file_into_chunks(str(KNOWLEDGE_FILE_PATH))
        clear_vectorstore()
        populate_vectorstore(knowledge_chunks)

    except (FileNotFoundError, ValueError, EnvironmentError) as e:
        print(f"Error: {str(e)}")
