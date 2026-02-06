import spacy
import en_core_web_sm

nlp = en_core_web_sm.load()

def compute_similarity(clause_text, template_text):
    doc1 = nlp(clause_text)
    doc2 = nlp(template_text)

    return doc1.similarity(doc2)

