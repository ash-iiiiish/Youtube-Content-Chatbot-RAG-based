import os
from pathlib import Path
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# ── Load .env ─────────────────────────────────────────
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env", override=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise EnvironmentError(
        "GROQ_API_KEY not found. "
        "Make sure a .env file with GROQ_API_KEY=gsk_... exists in the project folder."
    )

# ── Initialize Groq Model ─────────────────────────────
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3,
    api_key=GROQ_API_KEY,
)

# ── Call LLM ──────────────────────────────────────────
def call_llm(final_prompt: str) -> str:
    """
    Calls Groq LLM using LangChain wrapper
    """

    response = llm.invoke(final_prompt)

    return response.content