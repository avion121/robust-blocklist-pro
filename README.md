# ROBUST-BLOCKLIST-PRO

**ROBUST-BLOCKLIST-PRO** is an advanced blocklist generator that aggregates trusted blocklists from multiple sources and consolidates them into a safe, standardized blocklist. It operates in a strict safe mode—only accepting host file style entries (converted to the format `||domain^`)—to ensure no legitimate websites are accidentally blocked. Additionally, it includes a rule to block popup redirects for enhanced browsing protection.

[![GitHub Actions Status](https://github.com/yourusername/ROBUST-BLOCKLIST-PRO/workflows/Deployment/badge.svg)](https://github.com/yourusername/ROBUST-BLOCKLIST-PRO/actions)

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Repository Structure](#repository-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Trusted Sources:** Aggregates blocklists from a curated list of reliable feeds.
- **Safe Mode Operation:** Accepts only rules in the safe format (`||domain^`), ensuring that legitimate websites remain unaffected.
- **Popup Redirect Protection:** Automatically adds an explicit rule to block popup redirects.
- **Automated Updates:** Uses a GitHub Actions workflow to generate and deploy the blocklist daily at 05:00 UTC.
- **Robust Error Handling:** Incorporates retry logic and error reporting for dependable source fetching.

## How It Works

1. **Fetching Sources:** Downloads blocklists from multiple trusted URLs.
2. **Normalization:** Converts host file style entries (e.g., `0.0.0.0 example.com`) into the standardized safe format (`||example.com^`).
3. **Safe Mode Filtering:** Only accepts rules that strictly match the safe format.
4. **Popup Redirect Rule:** Inserts an explicit rule to block popup redirects.
5. **Optimization:** Deduplicates and sorts the rules for an optimized final blocklist.
6. **Output Generation:** Writes the final consolidated blocklist to `robust-blocklist-pro.txt`.

## Repository Structure

- **`robust-blocklist-pro.py`**: The main Python script that aggregates, normalizes, and generates the consolidated blocklist.
- **`.github/workflows/deployment.yml`**: GitHub Actions workflow file for automated generation and deployment.
- **`robust-blocklist-pro.txt`**: (Generated) The final, consolidated blocklist output file.


