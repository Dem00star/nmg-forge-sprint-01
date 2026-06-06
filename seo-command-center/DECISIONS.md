# Engineering Decision & Architecture Log

### Phase 1: Data Ingestion Strategy
* **Decision:** Bypass LLM for raw data extraction; use pure `pandas`.
* **Rationale:** The `internal_all.csv` from Screaming Frog can contain tens of thousands of rows. Feeding this directly into a local LLM context window would guarantee token exhaustion, massive latency, and hallucinations. I opted to build a deterministic Python extractor (`seo_extractor.py`) to calculate `urls_crawled`, `4xx_errors`, and `missing_h1s`. The LLM is reserved strictly for high-level logic and report generation, satisfying the efficiency requirements.

### Phase 2: Enforcing the Output Contract
* **Decision:** Strict manual override of the JSON formatting script.
* **Rationale:** During the initial generation of `json_formatter.py`, the sub-agent utilized generic keys (e.g., `metricsOverview`, `keyFindings`). Recognizing that the auto-grader evaluates against a strict `report.schema.json` contract, I halted the pipeline and issued a corrective prompt to enforce exact nested structures (e.g., nesting `total_issues` under the `summary` key, and enforcing lowercase keys like `type` and `severity`). 

### Phase 3: Bypassing System Dependencies (PDF Generation)
* **Decision:** Pivot from `weasyprint` to `fpdf2` for PDF report generation.
* **Rationale:** The initial plan utilized `weasyprint` to convert HTML to PDF. However, execution on a macOS M-series environment failed due to missing native C-libraries (`libgobject`). Recognizing the strict 6-hour time limit, debugging C-compilers via Homebrew was a poor allocation of resources. I immediately pivoted the architecture to use `fpdf2`, a pure-Python library. This guarantees the script will execute flawlessly in a headless environment when the NMG judges run the code.

### Phase 4: Auditing LLM Hallucinations (PPTX & PDF)
* **Decision:** Manual code review and targeted reprompting to fix schema drift.
* **Rationale:** While generating the presentation and PDF scripts, the LLM hallucinated dictionary keys that did not exist in our extracted JSON (e.g., `site_key` instead of `site`, and `Type` instead of `type`). Allowing this to execute would result in `None` values or application crashes. I manually audited the generated Python code, identified the schema mismatch, and explicitly prompted the agent to correct the variables before testing.

### Phase 5: Master Orchestration
* **Decision:** Build a deterministic `main_pipeline.py` script.
* **Rationale:** Rather than relying on an unpredictable LLM prompt sequence to trigger the sub-agents one by one, I built a master Python pipeline that imports the modules and executes them sequentially. I then hijacked the provided `run.py` to route the grader's command-line argument (`sample-export/`) directly into this bulletproof pipeline, ensuring a 100% repeatable, crash-free execution.