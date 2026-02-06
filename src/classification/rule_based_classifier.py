from src.classification.contract_types import CONTRACT_TYPES

def classify_contract_rule_based(text):
    text_lower = text.lower()
    scores = {}

    for contract_type, keywords in CONTRACT_TYPES.items():
        score = 0
        for keyword in keywords:
            if keyword in text_lower:
                score += 1
        scores[contract_type] = score

    best_type = max(scores, key=scores.get)
    confidence = scores[best_type] / (len(CONTRACT_TYPES[best_type]) or 1)

    return best_type, round(confidence, 2), scores
