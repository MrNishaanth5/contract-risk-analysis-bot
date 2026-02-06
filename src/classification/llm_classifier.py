def classify_contract_llm(text, llm):
    prompt = f"""
    Identify the contract type from the following text.
    Choose only one:
    - Employment Agreement
    - Lease Agreement
    - Service Agreement
    - Vendor Agreement
    - Partnership Deed

    Contract Text:
    {text[:3000]}
    """

    response = llm(prompt)
    return response.strip()
