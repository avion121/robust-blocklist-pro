#!/usr/bin/env python3
"""
ROBUST-BLOCKLIST-PRO Generator v3.3

This script aggregates multiple blocklists from various sources, including:

  • uBlock Origin Filters:
      - Ads:         https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/filters.txt
      - Badware:     https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/badware.txt
      - Privacy:     https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/privacy.txt
      - Quick Fixes: https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/quick-fixes.txt
      - Unbreak:     https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/unbreak.txt

  • EasyList & Easy Privacy:
      - EasyList:    https://easylist.to/easylist/easylist.txt
      - Easy Privacy:https://easylist.to/easylist/easyprivacy.txt

  • Online Malicious URL Blocklists:
      - Feodo Tracker:       https://feodotracker.abuse.ch/downloads/ipblocklist.txt
      - Ransomware Tracker:  https://ransomwaretracker.abuse.ch/downloads/RW_IPBL.txt
      - URLhaus hostfile:    https://urlhaus.abuse.ch/downloads/hostfile/

  • Peter Lowe's Ad and Tracking Server List:
      - Peter Lowe’s:         https://raw.githubusercontent.com/StevenBlack/hosts/master/data/peter-lowe.txt

  • Additional Sources:
      - Core Protection:
          • Hagezi:         https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.txt
          • Fake News:      https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling/hosts
          • big.oisd:       https://big.oisd.nl
          • 1Hosts:         https://raw.githubusercontent.com/badmojr/1Hosts/master/Lite/adblock.txt
      - Enhanced Security:
          • Adguard Mobile: https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_11_Mobile/filter.txt
          • Spam404:        https://raw.githubusercontent.com/Spam404/lists/master/main-blacklist.txt
          • NoTrack:        https://gitlab.com/quidsup/notrack-blocklists/-/raw/master/malware.hosts

The script fetches each list with retry logic and writes them (with header metadata and source annotations) to 'robust-blocklist-pro.txt'.
"""

import sys
from datetime import datetime
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# All provided blocklist URLs (duplicates will be removed)
FILTER_LIST_URLS = [
    # uBlock Origin Filters
    "https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/filters.txt",       # Ads
    "https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/badware.txt",       # Badware risks
    "https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/privacy.txt",       # Privacy
    "https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/quick-fixes.txt",     # Quick fixes
    "https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/unbreak.txt",         # Unbreak

    # EasyList & Easy Privacy
    "https://easylist.to/easylist/easylist.txt",                                                # EasyList
    "https://easylist.to/easylist/easyprivacy.txt",                                             # Easy Privacy

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

def deduplicate_preserve_order(urls):
    """Remove duplicate URLs while preserving the original order."""
    seen = set()
    unique = []
    for url in urls:
        if url not in seen:
            seen.add(url)
            unique.append(url)
    return unique

def fetch_filter_list(url):
    """
    Fetch the content from the given URL using a session with retry logic.
    Returns the text content or None if an error occurs.
    """
    session = requests.Session()
    retry_policy = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry_policy)
    session.mount("https://", adapter)
    try:
        response = session.get(url, timeout=20)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None

def main():
    unique_urls = deduplicate_preserve_order(FILTER_LIST_URLS)
    combined_content = []
    
    # Header metadata
    combined_content.append("! Title: ROBUST-BLOCKLIST-PRO - Comprehensive Blocklist")
    combined_content.append("! Version: 3.3")
    combined_content.append(f"! Updated: {datetime.utcnow().isoformat()}")
    combined_content.append("! Description: Aggregated blocklists from multiple sources.")
    combined_content.append("")
    
    # Fetch each unique URL and append its content
    for url in unique_urls:
        print(f"Fetching: {url} ...")
        content = fetch_filter_list(url)
        if content:
            combined_content.append(f"! Source: {url}")
            combined_content.append(content)
            combined_content.append("")  # Separator between sources

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
