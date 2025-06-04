from app.backend.core.chromadb_client import collection
from app.backend.core.config import NUM_RETRIEVAL_TURNS, NUM_CONTEXT_CHUNKS

# ─────────────────────────────────────────────
# FUNCTION DEFINITIONS

def build_contextual_query(conversation):
    """Builds a retrieval query using the last 3 conversation turns."""

    return "\n".join(turn.get("content", "") for turn in conversation[-NUM_RETRIEVAL_TURNS:])


def retrieve_context_chunks(query):
    """Retrieves top context chunks from the vector store based on the query."""

    results = collection.query(query_texts=[query], n_results=NUM_CONTEXT_CHUNKS)
    documents = results.get("documents", [[]])[0] if results else []
    return "\n\n".join(documents)

