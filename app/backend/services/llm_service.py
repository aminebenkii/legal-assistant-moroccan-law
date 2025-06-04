from app.backend.core.openai_client import openai_client
from app.backend.core.config import LLM_PROMPT, LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS

# ─────────────────────────────────────────────
# FUNCTION DEFINITIONS

def prepare_llm_payload(conversation):
    """ Constructs the message payload for the LLM API."""
    messages = [{"role": "system", "content": f"{LLM_PROMPT}"}] + conversation
    return messages
    


def generate_llm_response(messages):
    """ Calls the LLM API and returns the generated response."""
    try:
        response = openai_client.chat.completions.create(
            model=LLM_MODEL or "gpt-4o-mini",
            messages=messages,
            temperature=LLM_TEMPERATURE or 0.3,
            max_tokens=LLM_MAX_TOKENS or 500
        )

        print("number of cached tokens:", response.usage.prompt_tokens_details.cached_tokens)
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error occurred while generating response: {str(e)}"
