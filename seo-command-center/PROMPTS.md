# Key Prompts & Iteration Log

### 1. Data Extraction (Initial Success)
* **Prompt:** "Create a new file at `seo-command-center/scripts/seo_extractor.py`. Write a Python function called `extract_seo_metrics(csv_path)` that uses the pandas library to read a CSV file. The function must calculate and return a dictionary containing exactly: total_pages, 4xx_errors, and missing_h1s."
* **Result:** Succeeded on the first attempt. The agent correctly utilized `pandas` vectorization to handle potential `NaN` and whitespace issues securely without LLM hallucinations.

### 2. The JSON Schema Correction (Revision Required)
* **Initial Issue:** The agent formatted the output using generic keys instead of the required schema.
* **Corrective Prompt:** "Rewrite the `seo-command-center/scripts/json_formatter.py` file completely. The `format_report(metrics_dict)` function must return a JSON string that strictly adheres to the `report.schema.json` contract. Construct a Python dictionary with exactly these root keys: `site`, `urls_crawled`, `summary`, `issues`, and `run_meta`."
* **Result:** The explicit constraint forced the agent to abandon its generic structure and perfectly map the extracted data to the grading harness's expected JSON format.

### 3. The PDF Library Pivot (Critical Fix)
* **Initial Issue:** `weasyprint` failed due to missing macOS C-libraries.
* **Corrective Prompt:** "The `weasyprint` library failed due to missing system C-libraries on macOS. Rewrite the `seo-command-center/scripts/report_generator.py` file completely using `fpdf2` instead of `weasyprint`. The `generate_html_and_pdf(json_string)` function must parse the string and generate a PDF using FPDF, looping over the `issues` array."
* **Result:** Bypassed the system blocker. The agent successfully rewrote the HTML string logic and implemented a native Python PDF generation sequence.

### 4. Hallucination Fix (PPTX Generator)
* **Initial Issue:** Agent used `data.get('site_key')` which does not exist in our JSON output.
* **Corrective Prompt:** "Open `seo-command-center/scripts/pptx_generator.py` and fix a bug on line 13. Change `data.get('site_key', 'SEO Audit')` to `data.get('site', 'SEO Audit')` so it correctly matches our JSON schema. Output the updated code block only."
* **Result:** Instant targeted fix, ensuring the slide deck title pulled the correct URL string.