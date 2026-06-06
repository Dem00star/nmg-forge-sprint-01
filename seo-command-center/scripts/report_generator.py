import json
from fpdf import FPDF


def generate_html_and_pdf(json_string: str) -> None:
    """
    Parse a JSON string and generate:
      1. An HTML file (final_report.html)
      2. A PDF file (final_report.pdf) using fpdf2
    """
    try:
        data = json.loads(json_string)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON supplied: {exc}") from exc

    # ---------- HTML generation ----------
    html_parts = []
    site = data.get("site")
    if site:
        html_parts.append(f"<h1>{site}</h1>")

    urls_crawled = data.get("urls_crawled", "")
    if urls_crawled:
        html_parts.append(f"<p>Urls crawled: {urls_crawled}</p>")

    summary = data.get("summary", {})
    total_issues = summary.get("total_issues")
    if total_issues is not None:
        html_parts.append(f"<p>Total issues: {total_issues}</p>")

    issues = data.get("issues", [])
    if issues:
        html_parts.append("<ul>")
        for issue in issues:
            issue_type = issue.get("type", "")
            severity = issue.get("severity", "")
            count = issue.get("count", "")
            html_parts.append(f"<li>{issue_type}: {severity} - {count}</li>")
        html_parts.append("</ul>")

    html_output = "".join(html_parts)

    with open("final_report.html", "w", encoding="utf-8") as f:
        f.write(html_output)

    # ---------- PDF generation ----------
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=16)
    pdf.cell(0, 10, txt=site or "", ln=True)

    pdf.set_font("Arial", size=14)
    pdf.cell(0, 10, txt="Executive Summary", ln=True)

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt=str(urls_crawled), ln=True)
    pdf.cell(0, 10, txt=str(total_issues) if total_issues is not None else "", ln=True)

    for issue in issues:
        issue_type = issue.get("type", "")
        severity = issue.get("severity", "")
        count = issue.get("count", "")
        pdf.cell(0, 10, txt=f"{issue_type}: {severity} - {count}", ln=True)

    pdf.output("final_report.pdf")