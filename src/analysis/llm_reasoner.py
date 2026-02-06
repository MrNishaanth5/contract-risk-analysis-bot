import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_clause_explanation(clause_text, risk=None):
    prompt = f"""
    You are a legal assistant for Indian small business owners.
    Explain the following contract clause in simple business English.

    Clause:
    {clause_text}

    Risk Level: {risk if risk else "Not specified"}

    Explain:
    1. What this clause means
    2. Why it could be risky or safe
    3. What an SME should watch out for
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()


def generate_renegotiation_suggestion(clause_text):
    prompt = f"""
    You are a contract negotiation expert for Indian SMEs.
    Suggest a safer alternative wording for the following clause.

    Clause:
    {clause_text}

    Provide:
    - One safer alternative clause
    - Short justification
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()


def generate_contract_summary(contract_type, clauses, overall_risk):
    clause_samples = "\n".join(
        [f"- {c['clause_id']}: {c['text'][:200]}" for c in clauses[:5]]
    )

    prompt = f"""
    You are a legal analyst.
    Generate a simple business-friendly summary for an Indian SME.

    Contract Type: {contract_type}
    Overall Risk: {overall_risk}

    Sample Clauses:
    {clause_samples}

    Keep language simple and practical.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()
