from src.classification.rule_based_classifier import classify_contract_rule_based
from src.classification.llm_classifier import classify_contract_llm

def classify_contract(text, llm=None):
    rule_type, confidence, scores = classify_contract_rule_based(text)

    if confidence < 0.3 and llm:
        llm_type = classify_contract_llm(text, llm)
        return llm_type, "LLM", confidence

    return rule_type, "Rule-Based", confidence
