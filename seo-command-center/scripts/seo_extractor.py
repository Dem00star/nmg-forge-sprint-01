import pandas as pd
from urllib.parse import urlparse

def extract_seo_metrics(csv_path):
    """Champion Tier Extractor: Parses Screaming Frog CSV securely."""
    # Handle potential encoding issues from raw CSV exports
    try:
        df = pd.read_csv(csv_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(csv_path, encoding='latin1')

    # 1. Base Metrics
    urls_crawled = len(df)
    first_url = str(df['Address'].iloc[0]) if not df.empty and 'Address' in df.columns else "example.com"
    site_domain = urlparse(first_url).netloc if "http" in first_url else first_url

    metrics_dict = {
        "site_domain": site_domain,
        "urls_crawled": urls_crawled
    }

    issues_list = []

    # 2. Rulebook Detection: Missing Titles (High Severity)
    if 'Title 1' in df.columns and 'Status Code' in df.columns:
        # Rule: Title 1 empty on a 200 page
        missing_title_df = df[(df['Status Code'] == 200) & (df['Title 1'].isna() | (df['Title 1'] == ''))]
        if not missing_title_df.empty:
            issues_list.append({
                "type": "missing_title",
                "severity": "High",
                "affected_urls": missing_title_df['Address'].dropna().tolist(),
                "count": len(missing_title_df)
            })

    # 3. Rulebook Detection: Broken Links (High Severity)
    if 'Status Code' in df.columns:
        # Rule: Status Code 400-499
        broken_df = df[(df['Status Code'] >= 400) & (df['Status Code'] < 500)]
        if not broken_df.empty:
            issues_list.append({
                "type": "broken_link",
                "severity": "High",
                "affected_urls": broken_df['Address'].dropna().tolist(),
                "count": len(broken_df)
            })

    # 4. Rulebook Detection: Missing H1 (Medium Severity)
    if 'H1-1' in df.columns and 'Status Code' in df.columns:
        # Rule: H1-1 empty on a 200 page
        missing_h1_df = df[(df['Status Code'] == 200) & (df['H1-1'].isna() | (df['H1-1'] == ''))]
        if not missing_h1_df.empty:
            issues_list.append({
                "type": "missing_h1",
                "severity": "Medium",
                "affected_urls": missing_h1_df['Address'].dropna().tolist(),
                "count": len(missing_h1_df)
            })

    return metrics_dict, issues_list