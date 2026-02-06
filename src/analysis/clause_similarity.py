import spacy
from spacy.util import is_package
import subprocess
import sys

if not is_package("en_core_web_sm"):
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])

nlp = spacy.load("en_core_web_sm")

def compute_similarity(clause_text, template_text):
    doc1 = nlp(clause_text)
    doc2 = nlp(template_text)

    return doc1.similarity(doc2)


