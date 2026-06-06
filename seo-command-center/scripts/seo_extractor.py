import pandas as pd

def extract_seo_metrics(csv_path):
    df = pd.read_csv(csv_path)

    total_pages = len(df)

    # Count rows where "Status Code" starts with "4"
    # Convert to string first to handle potential numeric types
    errors_4xx = df[df['Status Code'].astype(str).str.startswith('4')].shape[0]

    # Count rows where "H1-1" is missing, blank, or NaN
    # pd.isna handles NaN; .strip() handles blanks/whitespace
    missing_h1s = df[df['H1-1'].isna() | (df['H1-1'].astype(str).str.strip() == '')].shape[0]

    return {
        "total_pages": total_pages,
        "4xx_errors": errors_4xx,
        "missing_h1s": missing_h1s
    }
