import os
import sys
import json
import csv
import time

# Import all sub-agent scripts
import seo_extractor
import json_formatter
import report_generator
import pptx_generator
import fix_generator

def update_dashboard_state(status_msg, progress_percent):
    """
    Step 4 Requirement: Writes state for the local MCP dashboard to consume.
    It mimics an SSE broadcast by writing to a local state file and printing to stdout.
    """
    print(f"[DASHBOARD_UPDATE] {progress_percent}% : {status_msg}")
    try:
        with open("mcp_state.json", "w", encoding="utf-8") as f:
            json.dump({"status": status_msg, "progress": progress_percent}, f)
    except Exception as e:
        print(f"Warning: Could not update dashboard state: {e}")

def export_champion_artifacts(fixes_dict, output_dir="outputs"):
    """
    Step 3 Requirement: Exports the AI-generated fixes to client-ready CSV artifacts.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Export Titles CSV
    titles = fixes_dict.get("titles", [])
    if titles:
        with open(os.path.join(output_dir, "fixes_titles.csv"), "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["url", "old", "new"])
            writer.writeheader()
            writer.writerows(titles)
            
    # Export Redirect Map CSV
    redirects = fixes_dict.get("redirect_map", [])
    if redirects:
        with open(os.path.join(output_dir, "fixes_redirects.csv"), "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["from", "to", "reason"])
            writer.writeheader()
            writer.writerows(redirects)

def main(csv_path):
    """Master orchestrator for the Champion Tier SEO pipeline."""
    start_time = time.time()
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    update_dashboard_state("Starting SEO Audit Pipeline...", 0)

    # 1. Deterministic Extraction
    update_dashboard_state("Ingesting CSV data...", 15)
    metrics_dict, issues_list = seo_extractor.extract_seo_metrics(csv_path)

    # 2. AI Fix Generation (Calling the new fix_generator.py)
    update_dashboard_state("AI generating title fixes and redirect maps...", 45)
    fixes_dict = fix_generator.generate_all_fixes(issues_list)

    # 3. Strict JSON Formatting
    update_dashboard_state("Formatting strictly to schema...", 75)
    duration_sec = int(time.time() - start_time)
    
    # Pass metrics, issues, fixes, and duration to the formatter
    json_payload = json_formatter.format_report(metrics_dict, issues_list, fixes_dict, duration_sec)
    
    # Write the master JSON contract
    with open(os.path.join(output_dir, "report.json"), "w", encoding="utf-8") as f:
        f.write(json_payload)

    # 4. Generate Final Deliverables (PDF, HTML, PPTX, and CSV Fixes)
    update_dashboard_state("Exporting client deliverables...", 90)
    report_generator.generate_html_and_pdf(json_payload)
    pptx_generator.generate_pptx(json_payload)
    
    # Trigger the CSV artifact generator
    export_champion_artifacts(fixes_dict, output_dir)

    update_dashboard_state("Audit Complete!", 100)
    print("✅ Pipeline execution finished successfully.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Please provide the path to internal_all.csv")