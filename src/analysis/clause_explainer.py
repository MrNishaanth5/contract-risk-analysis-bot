from src.llm.gemini_client import ask_gemini

SYSTEM_PROMPT = """
You are a legal assistant for Indian SMEs.
Explain contract clauses in simple business English.
Do NOT give legal advice.
"""

def explain_clause(clause_text: str) -> str:
    user_prompt = f"""
Explain the following contract clause in simple terms for a small business owner in India:

Clause:
{clause_text}
"""
    return ask_gemini(SYSTEM_PROMPT, user_prompt)
