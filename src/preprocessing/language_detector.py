import langid

def detect_language(text: str) -> str:
    try:
        lang, _ = langid.classify(text)
        return lang
    except:
        return "unknown"