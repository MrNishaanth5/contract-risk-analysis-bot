OBLIGATION_TERMS = [
    "shall", "must", "is required to", "agrees to"
]

RIGHT_TERMS = [
    "may", "is entitled to", "has the right to"
]

PROHIBITION_TERMS = [
    "shall not", "must not", "is prohibited from", "may not"
]

def classify_clause_role(text):
    text = text.lower()

    for term in PROHIBITION_TERMS:
        if term in text:
            return "Prohibition"

    for term in OBLIGATION_TERMS:
        if term in text:
            return "Obligation"

    for term in RIGHT_TERMS:
        if term in text:
            return "Right"

    return "Neutral"
