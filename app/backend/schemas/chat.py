from pydantic import BaseModel 

# ─────────────────────────────────────────────
# DATA MODELS :
class ChatRequest(BaseModel):
    sessionId : str
    query : str
    currency : Literal["EUR", "USD", "MAD"] = "EUR"

class ChatResponse(BaseModel):
    sessionId : str
    answer : str
