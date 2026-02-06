def suggest_mitigation(issue):
    if issue["issue"] == "Non-Indian jurisdiction":
        return "Consider changing governing law and jurisdiction to India to reduce enforcement cost."

    if issue["issue"] == "Non-compete clauses often unenforceable in India":
        return "Replace non-compete with confidentiality or non-solicitation clauses."
