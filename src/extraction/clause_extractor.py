import re

def extract_title(clause_text):
    lines = clause_text.split("\n")
    first_line = lines[0].strip()

    if len(first_line) < 80:
        return first_line.upper()

    return "GENERAL"

def fallback_sentence_split(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    clauses = []

    for i, sent in enumerate(sentences):
        if len(sent.strip()) > 100:
            clauses.append({
                "clause_id": f"F{i+1}",
                "title": "UNNUMBERED CLAUSE",
                "text": sent.strip()
            })

    return clauses

def extract_clauses(text):
    """
    Main clause extraction function.
    Tries numbered clauses first.
    Falls back to sentence-based splitting if needed.
    """

    pattern = r'\n(?=\d+(\.\d+)*\s)'
    raw_clauses = re.split(pattern, text)

    clauses = []
    clause_id = 1

    for clause in raw_clauses:
        clause = clause.strip()
        if len(clause) < 30:
            continue

        clauses.append({
            "clause_id": f"C{clause_id}",
            "title": extract_title(clause),
            "text": clause
        })
        clause_id += 1

    # 🔁 FALLBACK LOGIC
    if len(clauses) < 3:
        clauses = fallback_sentence_split(text)

    return clauses
