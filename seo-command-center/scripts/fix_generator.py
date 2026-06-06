import requests
import json
import urllib.parse

OLLAMA_API_URL = "http://localhost:11434/api/generate"
# Adjust model name based on your Track (e.g., qwen3.5:9b or gemma4:31b-cloud)
MODEL_NAME = "qwen3.5:9b" 

def generate_title_fix(url):
    """Uses local LLM to generate a compliant SEO title."""
    prompt = f"You are an expert SEO analyst. Write a highly clickable, SEO-optimized page title for the URL: {url}. It MUST be under 60 characters. Output ONLY the new title text, nothing else."
    
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json().get("response", "").strip('"\'\n')
        return "Needs Manual Review"
    except Exception as e:
        print(f"LLM Error on {url}: {e}")
        return "LLM Generation Failed"

def build_redirect_map(broken_urls):
    """Maps 4xx errors to the closest parent directory."""
    redirects = []
    for url in broken_urls:
        parsed = urllib.parse.urlparse(url)
        path_parts = [p for p in parsed.path.split('/') if p]
        
        # Simple heuristic: redirect to parent directory or homepage
        if len(path_parts) > 1:
            new_path = '/' + '/'.join(path_parts[:-1]) + '/'
        else:
            new_path = '/'
            
        target_url = urllib.parse.urlunparse((parsed.scheme, parsed.netloc, new_path, '', '', ''))
        redirects.append({
            "from": url,
            "to": target_url,
            "reason": "404 -> closest live parent"
        })
    return redirects

def generate_all_fixes(issues_list):
    """Parses issues and generates the Champion Tier 'fixes' dictionary."""
    fixes = {"titles": [], "redirect_map": []}
    
    for issue in issues_list:
        if issue.get("type") in ["missing_title", "title_too_long"]:
            print(f"🤖 AI generating fixes for {len(issue.get('affected_urls', []))} titles...")
            for url in issue.get("affected_urls", []):
                new_title = generate_title_fix(url)
                fixes["titles"].append({"url": url, "old": "N/A", "new": new_title})
                
        if issue.get("type") == "broken_link":
            print("🗺️ Building redirect map for broken links...")
            fixes["redirect_map"] = build_redirect_map(issue.get("affected_urls", []))
            
    return fixes