def check_indian_compliance(clauses):
    issues = []

    for clause in clauses:
        text = clause["text"].lower()

        if "jurisdiction" in text and "india" not in text:
            issues.append({
                "clause_id": clause["clause_id"],
                "issue": "Non-Indian jurisdiction",
                "risk": "HIGH"
            })

        if "non-compete" in text:
            issues.append({
                "clause_id": clause["clause_id"],
                "issue": "Non-compete clauses often unenforceable in India",
                "risk": "VERY HIGH"
            })

    return issues
