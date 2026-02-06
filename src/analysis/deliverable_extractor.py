def extract_deliverables(text):
    keywords = [
        "deliverable",
        "milestone",
        "service level",
        "performance",
        "timeline",
        "completion"
    ]

    found = []
    text_lower = text.lower()

    for key in keywords:
        if key in text_lower:
            found.append(key)

    return {
        "has_deliverables": bool(found),
        "keywords": found
    }
