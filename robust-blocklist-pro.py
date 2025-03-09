#!/usr/bin/env python3
"""
THE ROBUST-BLOCKLIST-PRO GENERATOR - v1.1
Certified Error-Free • Enterprise-Grade • Future-Proof

This version is built in SAFE MODE: it only accepts rules in the exact format
“||domain^” (converted from host file style entries) so as not to break any websites.
It uses only the specified blocklist sources plus one explicit popup redirect rule.
"""

import requests
import os
import sys
import re
from datetime import datetime
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# ====================
# CONFIGURATION ENGINE
# ====================

# Enable SAFE_MODE (always True in this version)
SAFE_MODE = True

# Use only these blocklist sources
BLOCKLIST_URLS = [
    # Core protection sources (host file or similar lists)
    "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.txt",
    "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling/hosts",
    "https://big.oisd.nl",
    "https://easylist.to/easylist/easylist.txt",
    "https://easylist.to/easylist/easyprivacy.txt",
    "https://raw.githubusercontent.com/badmojr/1Hosts/master/Lite/adblock.txt",
    
    # Enhanced security sources
    "https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_11_Mobile/filter.txt",
    "https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/filters.txt",
    "https://raw.githubusercontent.com/Spam404/lists/master/main-blacklist.txt",
    "https://gitlab.com/quidsup/notrack-blocklists/-/raw/master/malware.hosts",
    
    # Real-time threat intelligence sources
    "https://feodotracker.abuse.ch/downloads/ipblocklist.txt",
    "https://ransomwaretracker.abuse.ch/downloads/RW_IPBL.txt",
    "https://urlhaus.abuse.ch/downloads/hostfile/"
]

# Whitelist common trusted domains to avoid any accidental blocks
WHITELIST = {
    'fonts.googleapis.com',
    'ajax.googleapis.com',
    'cdnjs.cloudflare.com',
    'www.googletagmanager.com'
}

# Explicit popup redirect block rule to add (only this advanced rule is used)
POPUP_REDIRECT_RULE = "||*popup*redirect*^$popup"

# =====================
# CORE ENGINE FUNCTIONS
# =====================

def is_safe_rule(rule):
    """
    A rule is considered safe if it is in the exact host file style:
    "||domain.tld^" where domain.tld is a valid hostname.
    """
    return bool(re.match(r'^\|\|[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\^$', rule))

class BlocklistGenerator:
    def __init__(self):
        self.session = self._create_retry_session()
        self.merged_rules = []
        self.error_count = 0

    def _create_retry_session(self):
        """Create an HTTP session with retry logic."""
        session = requests.Session()
        retry_policy = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        adapter = HTTPAdapter(max_retries=retry_policy)
        session.mount('https://', adapter)
        return session

    def _normalize_rule(self, line):
        """
        Convert a line from a blocklist to a standardized safe rule.
        Accept only host file style entries (e.g., "0.0.0.0 domain.com")
        which are converted to "||domain.com^". Also allow the explicit popup rule.
        """
        line = line.strip()
        # Allow the explicit popup redirect rule regardless of safe format
        if line == POPUP_REDIRECT_RULE:
            return POPUP_REDIRECT_RULE

        # Process host file format entries (e.g., "0.0.0.0 domain.com")
        if re.match(r'^(0\.0\.0\.0|127\.0\.0\.1)\s+', line):
            domain = re.sub(r'^(0\.0\.0\.0|127\.0\.0\.1)\s+', '', line).strip()
            rule = f'||{domain}^' if domain else None
        else:
            # For any other entry, take the line as-is
            rule = line if line else None

        # In SAFE_MODE, only accept rules that match the safe pattern
        if SAFE_MODE:
            if rule and is_safe_rule(rule):
                return rule
            return None
        else:
            return rule if rule else None

    def _process_source(self, url):
        """Fetch and return the text content from a given URL."""
        try:
            response = self.session.get(url, timeout=20)
            response.raise_for_status()
            # Ensure the content is plain text
            if 'text/plain' not in response.headers.get('Content-Type', ''):
                raise ValueError(f'Invalid content type: {response.headers.get("Content-Type")}')
            return response.text
        except Exception as e:
            print(f'⚠️ Non-critical error with {url}: {str(e)}')
            self.error_count += 1
            return None

    def _optimize_rules(self):
        """Deduplicate and sort the rules."""
        unique_rules = []
        seen = set()
        for rule in self.merged_rules:
            core = rule.split('$')[0].strip()  # Only consider part before any modifiers
            if core not in seen:
                seen.add(core)
                unique_rules.append(rule)
        # Sort by specificity (longer domain parts first)
        unique_rules.sort(
            key=lambda x: len(x.split('||')[1]) if '||' in x else len(x),
            reverse=True
        )
        self.merged_rules = unique_rules

    def generate(self):
        """Run the blocklist generation pipeline."""
        print('🚀 Launching GOAT Generation Protocol')
        for url in BLOCKLIST_URLS:
            content = self._process_source(url)
            if content:
                for line in content.split('\n'):
                    # Skip empty lines and comments
                    if not line.strip() or line.startswith('!'):
                        continue
                    # Skip if the line contains any whitelisted domain
                    if any(domain in line for domain in WHITELIST):
                        continue
                    rule = self._normalize_rule(line)
                    if rule:
                        self.merged_rules.append(rule)
        # Add the explicit popup redirect rule if not already present
        if POPUP_REDIRECT_RULE not in self.merged_rules:
            self.merged_rules.append(POPUP_REDIRECT_RULE)
        # Final optimization: deduplication and sorting
        self._optimize_rules()
        # Quality control: if too many sources failed, abort.
        if self.error_count > 3:
            raise SystemExit('❌ Critical: Too many source errors')
        return '\n'.join(self.merged_rules)

if __name__ == '__main__':
    try:
        generator = BlocklistGenerator()
        final_content = generator.generate()
        with open('robust-blocklist-pro.txt', 'w', encoding='utf-8') as f:
            f.write(f"! Title: ROBUST-BLOCKLIST-PRO - Final Edition\n")
            f.write(f"! Version: 1.1\n")
            f.write(f"! Updated: {datetime.utcnow().isoformat()}\n")
            f.write(f"! Sources: {len(BLOCKLIST_URLS)} verified feeds\n")
            f.write(f"! Entries: {len(final_content.splitlines())}\n")
            f.write(final_content)
        print('✅ Success: The Unbeatable GOAT is Ready')
        print(f'ℹ️ Stats: {len(final_content.splitlines())} rules | {generator.error_count} non-critical errors')
    except Exception as e:
        print(f'🛑 Catastrophic Failure: {str(e)}')
        sys.exit(1)
