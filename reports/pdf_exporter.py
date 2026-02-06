from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors
from datetime import datetime


def export_pdf(report_data, output_path="contract_analysis_report.pdf"):
    """
    report_data: dict with keys
        - summary (str)
        - contract_type (str)
        - overall_risk (str)
        - clause_risks (list of dicts)
        - compliance_issues (list of dicts)
        - disclaimer (str)
    """

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    styles["Normal"].alignment = TA_LEFT

    elements = []


    # Title
    elements.append(
        Paragraph(
            "<b>Contract Analysis & Risk Assessment Report</b>",
            styles["Title"]
        )
    )
    elements.append(Spacer(1, 12))

    # Metadata
    metadata_text = f"""
    <b>Contract Type:</b> {report_data.get("contract_type", "N/A")}<br/>
    <b>Overall Risk Level:</b> {report_data.get("overall_risk", "N/A")}<br/>
    <b>Generated On:</b> {datetime.now().strftime('%d-%m-%Y %H:%M')}
    """
    elements.append(Paragraph(metadata_text, styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Summary Section
    elements.append(Paragraph("<b>1. Simplified Contract Summary</b>", styles["Heading2"]))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(report_data.get("summary", "No summary available."), styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Clause Risk Table
    elements.append(Paragraph("<b>2. Clause-Level Risk Assessment</b>", styles["Heading2"]))
    elements.append(Spacer(1, 6))

    clause_table_data = [
        ["Clause ID", "Risk Level", "Reason"]
    ]

    for clause in report_data.get("clause_risks", []):
        clause_table_data.append([
            clause.get("clause_id", "-"),
            clause.get("risk", "-"),
            clause.get("reason", "-")
        ])

    clause_table = Table(
        clause_table_data,
        colWidths=[70, 80, 300]
    )

    clause_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONT", (0, 0), (-1, 0), "Helvetica-Bold")
    ]))

    elements.append(clause_table)
    elements.append(Spacer(1, 12))

    # Compliance Issues
    elements.append(Paragraph("<b>3. Indian Compliance Issues</b>", styles["Heading2"]))
    elements.append(Spacer(1, 6))

    compliance_issues = report_data.get("compliance_issues", [])

    if not compliance_issues:
        elements.append(Paragraph("No major compliance issues detected.", styles["Normal"]))
    else:
        for issue in compliance_issues:
            issue_text = f"""
            <b>Clause:</b> {issue.get("clause_id", "N/A")}<br/>
            <b>Issue:</b> {issue.get("issue", "")}<br/>
            <b>Risk:</b> {issue.get("risk", "")}<br/>
            <b>Suggested Mitigation:</b> {issue.get("mitigation", "")}
            """
            elements.append(Paragraph(issue_text, styles["Normal"]))
            elements.append(Spacer(1, 8))

    elements.append(Spacer(1, 12))

    # Disclaimer
    elements.append(Paragraph("<b>4. Legal Disclaimer</b>", styles["Heading2"]))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(report_data.get("disclaimer", ""), styles["Normal"]))

    # Build PDF
    doc.build(elements)

    return output_path
