# ROBUST-BLOCKLIST-PRO

**ROBUST-BLOCKLIST-PRO** is an advanced blocklist generator that aggregates trusted blocklists from multiple sources, converts them into a safe, standardized format, and outputs a consolidated blocklist. It is designed to ensure no legitimate websites are broken by operating in a strict safe mode—only host file style entries (converted to the format `||domain^`) are accepted. In addition, it adds a specific rule to block popup redirects.

## Features

- **Trusted Sources:** Uses a curated list of blocklist sources.
- **Safe Mode:** Accepts only rules in the exact format `||domain^` (converted from host file entries) to prevent accidental blocking of legitimate websites.
- **Popup Redirect Block:** Includes an explicit rule to block popup redirects.
- **Automated Deployment:** GitHub Actions workflow for daily (05:00 UTC) automated updates.
- **Robust Error Handling:** Built-in retry logic and error reporting for reliable source fetching.

## How It Works

1. **Fetching Sources:** The script downloads blocklists from a set list of URLs.
2. **Normalization:** Converts host file style entries (e.g., `0.0.0.0 example.com`) into the safe format (`||example.com^`).
3. **Safe Mode Filtering:** Only rules matching the strict safe format are accepted.
4. **Popup Redirect Rule:** Adds an explicit rule to block popup redirects.
5. **Optimization:** Deduplicates and sorts rules to create an optimized final blocklist.
6. **Output:** Writes the final blocklist to `robust-blocklist-pro.txt`.

## Repository Structure

- **`robust-blocklist-pro.py`**: The main Python script that generates the blocklist.
- **`.github/workflows/deployment.yml`**: GitHub Actions workflow file for automated generation and deployment.
- **`robust-blocklist-pro.txt`**: (Generated) The final, consolidated blocklist.

