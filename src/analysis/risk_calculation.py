def calculate_overall_risk(clauses, compliance_issues):
    high = 0
    medium = 0

    for clause in clauses:
        if clause.get("risk") == "HIGH":
            high += 1
        elif clause.get("risk") == "MEDIUM":
            medium += 1

    if high > 0 or len(compliance_issues) > 0:
        return "HIGH"
    elif medium > 2:
        return "MEDIUM"
    else:
        return "LOW"
