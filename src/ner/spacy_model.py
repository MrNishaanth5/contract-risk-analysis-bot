import spacy
from spacy.util import is_package
import subprocess
import sys

def load_spacy_model():
    if not is_package("en_core_web_sm"):
        subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")
    return nlp

nlp = load_spacy_model()
