#!/usr/bin/env python3
"""
ROBUST-BLOCKLIST-PRO Generator v3.3 Deeply Modified (Stealth Mode)

This script aggregates multiple blocklists from various sources using advanced
stealth techniques to mimic human browsing behavior. It rotates through a set
of common browser User-Agent strings, uses a persistent session with a retry
policy, and introduces randomized delays between requests.

Note: While these measures can make the fetching process appear more natural,
they do not conceal the fact that the adblocking rules are in effect on client pages.
"""

import sys
import random
import time
from datetime import datetime
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# List of blocklist URLs (duplicates will be removed)
FILTER_LIST_URLS = [
    # uBlock Origin Filters
    "https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/filters.txt",
    "https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/badware.txt",
    "https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/privacy.txt",
    "https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/quick-fixes.txt",
    "https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/unbreak.txt",
    # EasyList & Easy Privacy
    "https://easylist.to/easylist/easylist.txt",
    "https://easylist.to/easylist/easyprivacy.txt",
    # Online Malicious URL Blocklists
    "https://feodotracker.abuse.ch/downloads/ipblocklist.txt",
    "https://ransomwaretracker.abuse.ch/downloads/RW_IPBL.txt",
    "https://urlhaus.abuse.ch/downloads/hostfile/",
    # Peter Lowe's ad and tracking server list
    "https://raw.githubusercontent.com/StevenBlack/hosts/master/data/peter-lowe.txt",
    # Core protection sources
    "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.txt",
    "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling/hosts",
    "https://big.oisd.nl",
    "https://raw.githubusercontent.com/badmojr/1Hosts/master/Lite/adblock.txt",
    # Enhanced security sources
    "https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_11_Mobile/filter.txt",
    "https://raw.githubusercontent.com/Spam404/lists/master/main-blacklist.txt",
    "https://gitlab.com/quidsup/notrack-blocklists/-/raw/master/malware.hosts"
]

# A pool of common browser User-Agent strings to randomize requests.
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
]

def deduplicate_preserve_order(urls):
    """Remove duplicate URLs while preserving the original order."""
    seen = set()
    unique = []
    for url in urls:
        if url not in seen:
            seen.add(url)
            unique.append(url)
    return unique

def create_session():
    """Create a persistent session with a robust retry policy."""
    session = requests.Session()
    retry_policy = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry_policy)
    session.mount("https://", adapter)
    return session

def fetch_filter_list(session, url):
    """
    Fetch the content from the given URL using a randomly chosen User-Agent.
    Returns the text content or None if an error occurs.
    """
    user_agent = random.choice(USER_AGENTS)
    headers = {
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br"
    }
    try:
        response = session.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching {url} with User-Agent {user_agent}: {e}", file=sys.stderr)
        return None

def main():
    unique_urls = deduplicate_preserve_order(FILTER_LIST_URLS)
    combined_content = []
    
    # Metadata header for the generated blocklist
    combined_content.append("! Title: ROBUST-BLOCKLIST-PRO - Comprehensive Blocklist")
    combined_content.append("! Version: 3.3 Deeply Modified")
    combined_content.append(f"! Updated: {datetime.utcnow().isoformat()}")
    combined_content.append("! Description: Aggregated blocklists from multiple sources using advanced stealth techniques.")
    combined_content.append("")
    
    session = create_session()
    
    for url in unique_urls:
        print(f"Fetching: {url} ...")
        content = fetch_filter_list(session, url)
        if content:
            combined_content.append(f"! Source: {url}")
            combined_content.append(content)
            combined_content.append("")  # Separator between sources
        # Introduce a random delay (1 to 5 seconds) to mimic human browsing behavior
        time.sleep(random.uniform(1, 5))
    
    output_filename = "robust-blocklist-pro.txt"
    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write("\n".join(combined_content))
        print("✅ Filter list updated successfully.")
    except Exception as e:
        print(f"Error writing to {output_filename}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
