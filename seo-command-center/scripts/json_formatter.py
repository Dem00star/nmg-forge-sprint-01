import json

def format_report(metrics_dict, issues_list, fixes_dict, duration_sec):
    """
    Compiles the final JSON payload adhering strictly to report.schema.json,
    including the Champion Tier fixes and dynamic recommendations blocks.
    """
    
    # Calculate totals deterministically
    total_issues = sum(issue.get("count", 0) for issue in issues_list)
    high_count = sum(i["count"] for i in issues_list if i.get("severity") == "High")
    medium_count = sum(i["count"] for i in issues_list if i.get("severity") == "Medium")
    low_count = sum(i["count"] for i in issues_list if i.get("severity") == "Low")

    # Generate dynamic recommendations based on AI fixes
    recs = []
    if high_count > 0:
        recs.append(f"CRITICAL: Address the {high_count} High-severity issues immediately to prevent indexation drops.")
    if len(fixes_dict.get("redirect_map", [])) > 0:
        recs.append("Implement the attached 301 redirect map in your .htaccess or Nginx config to recover lost link equity from broken internal links.")

    # Assemble the strict contract payload
    report_payload = {
        "site": metrics_dict.get("site_domain", "example.com"),
        "urls_crawled": metrics_dict.get("urls_crawled", 0),
        "summary": {
            "total_issues": total_issues,
            "by_severity": {
                "High": high_count,
                "Medium": medium_count,
                "Low": low_count
            }
        },
        "issues": issues_list,
        "fixes": fixes_dict,
        "recommendations": recs,
        "run_meta": {
            "model": "qwen3.5:9b", 
            "model_calls": len(fixes_dict.get("titles", [])),
            "duration_sec": duration_sec
        }
    }
    
    return json.dumps(report_payload, indent=2)