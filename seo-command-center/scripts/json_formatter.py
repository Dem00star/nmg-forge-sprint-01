import json
from datetime import date

def format_report(metrics_dict):
    """
    Formats SEO metrics into a JSON string adhering to the report.schema.json contract.
    """
    total_pages = metrics_dict.get("total_pages", 0)
    four_xx_errors = metrics_dict.get("4xx_errors", 0)
    missing_h1s = metrics_dict.get("missing_h1s", 0)

    total_issues = four_xx_errors + missing_h1s

    report = {
        "site": "https://nmgtechnologies.com",
        "urls_crawled": total_pages,
        "summary": {
            "total_issues": total_issues,
            "by_severity": {
                "High": four_xx_errors,
                "Medium": missing_h1s,
                "Low": 0
            }
        },
        "issues": [],
        "run_meta": {
            "timestamp": date.today().isoformat()
        }
    }

    if four_xx_errors > 0:
        report["issues"].append({
            "type": "broken_link",
            "severity": "High",
            "affected_urls": [],
            "count": four_xx_errors
        })

    if missing_h1s > 0:
        report["issues"].append({
            "type": "missing_h1",
            "severity": "Medium",
            "affected_urls": [],
            "count": missing_h1s
        })

    return json.dumps(report, indent=2)
