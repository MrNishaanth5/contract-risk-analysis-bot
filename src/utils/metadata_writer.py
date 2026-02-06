import json

def write_metadata(language):
    metadata={
    "orginal_language":language,
    "normalized_language": "en",
    "translation_used": language == "hi"
    }

    with open("data/extracted_text/metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata,f,indent=2)

def classify_metadata(final_type,method,confidence):
    classification_result = {
        "contract_type": final_type,
        "method": method,
        "confidence": confidence
    }

    with open("data/extracted_text/contract_type.json", "w") as f:
        json.dump(classification_result, f, indent=2)

def clause_metadata(clauses):
    with open("data/extracted_text/clauses.json", "w", encoding="utf-8") as f:
        json.dump(clauses, f, indent=2, ensure_ascii=False)

def entity_clause_metadata(clauses):
    with open("data/extracted_text/clauses_with_entities.json", "w", encoding="utf-8") as f:
        json.dump(clauses, f, indent=2, ensure_ascii=False)

def clause_role_metadata(clauses):
    with open("data/extracted_text/clauses_with_roles.json", "w", encoding="utf-8") as f:
        json.dump(clauses, f, indent=2, ensure_ascii=False)
