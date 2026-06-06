import os
import shutil
import seo_extractor
import json_formatter
import report_generator
import pptx_generator

def main(csv_path):
    # Create outputs folder in the root directory if it doesn't already exist
    if not os.path.exists('outputs'):
        os.makedirs('outputs')

    # Call seo_extractor.extract_seo_metrics(csv_path) and store the dictionary
    metrics = seo_extractor.extract_seo_metrics(csv_path)

    # Call json_formatter.format_report() with that dictionary to get the JSON string
    json_string = json_formatter.format_report(metrics)

    # Save that JSON string to a file at outputs/report.json
    with open('outputs/report.json', 'w') as f:
        f.write(json_string)

    # Call report_generator.generate_html_and_pdf(json_string)
    report_generator.generate_html_and_pdf(json_string)

    # Call pptx_generator.generate_pptx(json_string)
    pptx_generator.generate_pptx(json_string)

    # Move final_report.html, final_report.pdf, and final_report.pptx from the root directory into the outputs/ directory
    files_to_move = ['final_report.html', 'final_report.pdf', 'final_report.pptx']
    for file in files_to_move:
        if os.path.exists(file):
            shutil.move(file, os.path.join('outputs', file))

if __name__ == "__main__":
    main("sample-export/internal_all.csv")
