from src.preprocessing.translator import translate_hindi_to_english

def normalize_text(text,language,llm=None):
    if language == "hi":
        normalized_text= translate_hindi_to_english(text,llm)
    else:
        normalized_text=text
    
    return normalized_text