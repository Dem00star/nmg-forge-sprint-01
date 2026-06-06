# SEO Command Center: Project Memory & Constraints

### Global Directives
* **Goal:** Build an autonomous, offline Claude Code plugin that ingests a Screaming Frog SEO export, formats the data to a strict JSON contract, and generates a suite of client-ready deliverables (HTML, PDF, PPTX).
* **Environment:** Built for execution on local, free-tier tool-trained models.

### Architectural Constraints
* **Zero-LLM Data Parsing:** Do NOT feed the raw `internal_all.csv` rows into the LLM context window. All data parsing, aggregation, and threshold logic must be executed via deterministic Python code (e.g., `pandas`) to preserve tokens and guarantee accuracy against the NMG ground-truth grading metric.
* **Schema Adherence:** Output formatting is strictly governed by `report.schema.json`. Never invent new dictionary keys or alter casing (e.g., use `type`, never `Type`).
* **Dependency Management:** Avoid Python libraries that require deep system-level C-compilers (like `weasyprint`). Rely on pure-Python libraries (`fpdf2`, `python-pptx`) to ensure the solution executes flawlessly in the judge's isolated grading environment.

### Workflow Rules
* Always verify schema keys against `report.schema.json` before passing objects to the reporting generators.
* Log all critical tool failures in `DECISIONS.md`.
* Ensure `outputs/` directory is dynamically generated if missing before attempting file writes.