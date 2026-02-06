import streamlit as st

from src.utils.file_utils import save_uploaded_file
from src.ingestion.pdf_reader import extract_text_from_pdf
from src.ingestion.docx_reader import extract_text_from_doxc
from src.ingestion.txt_reader import extract_text_from_txt

from src.preprocessing.text_cleaner import clean_text
from src.preprocessing.language_detector import detect_language
from src.preprocessing.normalizer import normalize_text

from src.utils.metadata_writer import (
    write_metadata,
    classify_metadata,
    clause_metadata,
    entity_clause_metadata,
    clause_role_metadata
)

from src.classification.classifier import classify_contract
from src.extraction.clause_extractor import extract_clauses
from src.ner.entity_extractor import extract_entities
from src.analysis.role_classifier import classify_clause_role

from src.analysis.risk_calculation import calculate_overall_risk
from src.analysis.ambiguity_detector import detect_ambiguity
from src.analysis.clause_similarity import compute_similarity
from src.analysis.deliverable_extractor import extract_deliverables

from legal_rules.compliance_check import check_indian_compliance
from legal_rules.risk_mitigation import suggest_mitigation

from src.llm.gemini_client import ask_gemini

from reports.pdf_exporter import export_pdf
from audit.audit_logger import log_action

import spacy
from spacy.util import is_package
import subprocess
import sys

if not is_package("en_core_web_sm"):
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])

nlp = spacy.load("en_core_web_sm")


st.set_page_config(page_title="Contract Analysis & Risk Assessment Bot", layout="wide")
st.title("📄 Contract Analysis & Risk Assessment Bot")
st.write("Upload a **contract** to analyze risks, compliance, and SME impact.")

def extract_text(file_path):
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_text_from_doxc(file_path)
    elif file_path.endswith(".txt"):
        return extract_text_from_txt(file_path)
    else:
        return ""

uploaded_file = st.file_uploader(
    "Upload Contract",
    type=["pdf", "docx", "txt"]
)

if uploaded_file:
    file_path = save_uploaded_file(uploaded_file)
    st.success("File uploaded successfully")

    raw_text = extract_text(file_path)
    st.text_area("📄 Extracted Text (preview)", raw_text[:3000], height=250)

    cleaned_text = clean_text(raw_text)
    language = detect_language(cleaned_text)
    normalized_text = normalize_text(cleaned_text, language)

    write_metadata(language)

    final_type, method, confidence = classify_contract(normalized_text)

    st.subheader("📑 Contract Classification")
    st.write("**Type:**", final_type)
    st.write("**Method:**", method)
    st.write("**Confidence:**", confidence)

    classify_metadata(final_type, method, confidence)

    clauses = extract_clauses(normalized_text)
    st.subheader(f"🧩 Extracted Clauses ({len(clauses)})")

    with open("templates/termination_standard.txt", "r", encoding="utf-8") as f:
        termination_template = f.read()

    for clause in clauses[:5]:
        st.markdown(f"### {clause['clause_id']} — {clause['title']}")
        st.write(clause["text"])

        clause["entities"] = extract_entities(clause["text"])
        with st.expander("🔍 Extracted Entities"):
            st.json(clause["entities"])

        clause["role"] = classify_clause_role(clause["text"])
        st.write("**Clause Type:**", clause["role"])

        ambiguity = detect_ambiguity(clause["text"])
        clause["ambiguity"] = ambiguity
        if ambiguity["is_ambiguous"]:
            st.warning(f"⚠️ Ambiguous terms: {', '.join(ambiguity['terms'])}")

        similarity = compute_similarity(clause["text"], termination_template)
        clause["template_similarity"] = round(similarity, 2)
        if similarity < 0.65:
            st.info("ℹ️ Deviates from SME-friendly standard")

        deliverables = extract_deliverables(clause["text"])
        clause["deliverables"] = deliverables
        if deliverables["has_deliverables"]:
            st.success("📦 Deliverables / performance obligation detected")

        with st.expander("📘 Plain-language explanation"):
            explanation = ask_gemini(
                system_prompt="You explain legal clauses in simple business English for Indian SMEs.",
                user_prompt=clause["text"]
            )
            st.write(explanation)

        with st.expander("✏️ Renegotiation suggestion"):
            suggestion = ask_gemini(
                system_prompt="You suggest SME-friendly alternative contract wording.",
                user_prompt=clause["text"]
            )
            st.write(suggestion)

    clause_metadata(clauses)
    entity_clause_metadata(clauses)
    clause_role_metadata(clauses)

    compliance_issues = check_indian_compliance(clauses)
    for issue in compliance_issues:
        issue["mitigation"] = suggest_mitigation(issue)

    overall_risk = calculate_overall_risk(clauses, compliance_issues)

    st.subheader("⚠️ Overall Risk Assessment")
    st.write("**Composite Risk Level:**", overall_risk)

    summary = ask_gemini(
        system_prompt="Summarize contracts for Indian SME owners in simple English.",
        user_prompt=normalized_text[:4000]
    )

    st.subheader("📝 Contract Summary")
    st.write(summary)

    log_action(
        "CONTRACT_ANALYZED",
        {
            "contract_type": final_type,
            "overall_risk": overall_risk
        }
    )

    report_data = {
        "contract_type": final_type,
        "overall_risk": overall_risk,
        "summary": summary,
        "clauses": clauses,
        "compliance_issues": compliance_issues,
        "disclaimer": open("config/disclaimer.txt").read()
    }

    pdf_path = export_pdf(report_data)

    st.success("📄 PDF report generated")
    st.download_button(
        "Download Report",
        open(pdf_path, "rb"),
        file_name="contract_analysis_report.pdf"
    )

