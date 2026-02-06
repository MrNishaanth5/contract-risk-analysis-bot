def translate_hindi_to_english(text,llm):
    prompt=f"""
    Translate the following legal contract text from Hindi to clear,
    professional English. Preserve legal meaning.

    Text:
    {text}
    """
    responce= llm(prompt)
    return responce