def detect_ambiguity(text):
    ambiguous_terms = [
        "reasonable",
        "reasonably",
        "as soon as possible",
        "from time to time",
        "at the discretion",
        "material breach",
        "best efforts",
        "commercially reasonable",
        "subject to mutual agreement"
    ]

    found_terms = []
    text_lower = text.lower()

    for term in ambiguous_terms:
        if term in text_lower:
            found_terms.append(term)

    if found_terms:
        return {
            "is_ambiguous": True,
            "terms": found_terms,
            "risk": "MEDIUM",
            "reason": "Ambiguous language may lead to interpretation disputes"
        }

    return {
        "is_ambiguous": False,
        "terms": [],
        "risk": "LOW",
        "reason": ""
    }
