from src.ner.spacy_model import nlp

def compute_similarity(clause_text, template_text):
    doc1 = nlp(clause_text)
    doc2 = nlp(template_text)

    return doc1.similarity(doc2)



