import re
from src.ner.spacy_model import nlp

def extract_spacy_entities(text):
    doc = nlp(text)
    entities = {
        "DATE": [],
        "MONEY": [],
        "ORG": [],
        "GPE": []
    }

    for ent in doc.ents:
        if ent.label_ in entities:
            entities[ent.label_].append(ent.text)

    return entities

def extract_parties(text):
    pattern = r'(Employer|Employee|Company|Client|Vendor|Service Provider)'
    return list(set(re.findall(pattern, text, re.IGNORECASE)))

def extract_duration(text):
    pattern = r'\b\d+\s+(days|months|years)\b'
    return re.findall(pattern, text, re.IGNORECASE)

def extract_ip_terms(text):
    keywords = ["intellectual property", "ip rights", "copyright", "patent"]
    return [kw for kw in keywords if kw in text.lower()]

def extract_entities(text):
    spacy_entities = extract_spacy_entities(text)

    entities = {
        "parties": extract_parties(text),
        "dates": spacy_entities["DATE"],
        "money": spacy_entities["MONEY"],
        "jurisdiction": spacy_entities["GPE"],
        "duration": extract_duration(text),
        "ip": extract_ip_terms(text)
    }

    return entities



