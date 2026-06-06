import json
from weasyprint import HTML

def generate_html_and_pdf(json_string):
    """
    Parses a JSON string and generates an HTML report and a PDF version.
    """
    # Parse the JSON string into a dictionary
    data = json.loads(json_string)

    site_name = data.get('site', 'SEO Report')
    urls_crawled = data.get('urls_crawled', 0)
    summary = data.get('summary', {})
    total_issues = summary.get('total_issues', 0)
    issues = data.get('issues', [])

    # Create the issues list items
    issues_list_html = ""
    for issue in issues:
        issues_list_html += f"<li><strong>{issue.get('type', 'N/A')}</strong>: {issue.get('severity', 'N/A')} (Count: {issue.get('count', 0)})</li>"

    # HTML template with inline CSS
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                padding: 40px;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: auto;
            }}
            h1 {{
                color: #2c3e50;
                border-bottom: 2px solid #2c3e50;
                padding-bottom: 10px;
            }}
            .summary-box {{
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 30px;
            }}
            .summary-box h2 {{
                margin-top: 0;
                color: #495057;
            }}
            ul {{
                list-style-type: none;
                padding: 0;
            }}
            li {{
                padding: 10px 0;
                border-bottom: 1px solid #eee;
            }}
            li:last-child {{
                border-bottom: none;
            }}
            .severity-high {{ color: #d9534f; }}
            .severity-medium {{ color: #f0ad4e; }}
            .severity-low {{ color: #5bc0de; }}
        </style>
    </head>
    <body>
        <h1>{site_name}</h1>

        <div class="summary-box">
            <h2>Executive Summary</h2>
            <p><strong>URLs Crawled:</strong> {urls_crawled}</p>
            <p><strong>Total Issues Found:</strong> {total_issues}</p>
        </div>

        <h2>Issue Details</h2>
        <ul>
            {issues_list_html}
        </ul>
    </body>
    </html>
    """

    # Save HTML to root directory
    with open("final_report.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    # Convert HTML to PDF using weasyprint
    HTML(string=html_content).write_pdf("final_report.pdf")

    return "Reports generated successfully: final_report.html and final_report.pdf"
