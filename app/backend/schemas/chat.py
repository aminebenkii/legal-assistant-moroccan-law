from pydantic import BaseModel 

# ─────────────────────────────────────────────
# DATA MODELS :
class ChatRequest(BaseModel):
    sessionId : str
    query : str

class ChatResponse(BaseModel):
    sessionId : str
    answer : str
