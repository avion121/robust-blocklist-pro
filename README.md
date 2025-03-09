


# ROBUST-BLOCKLIST-PRO

**ROBUST-BLOCKLIST-PRO** is an advanced blocklist generator that aggregates and optimizes multiple blocklist sources into a single, consolidated file. Designed for enterprise-grade performance and future-proof protection, this project converts various blocklist formats into standardized AdBlock rules, injects advanced protections, and performs deduplication and optimization for enhanced efficiency.

## Features

- **Multi-Source Aggregation:** Retrieves blocklists from various trusted sources.
- **Standardization:** Converts host file and other rule formats into a consistent AdBlock syntax.
- **Advanced Protections:** Adds next-generation security rules for enhanced threat prevention.
- **Optimization Pipeline:** Deduplication, sorting by specificity, and wildcard compression ensure a lean, effective blocklist.
- **Automated Deployment:** Integrated with GitHub Actions for scheduled (daily at 05:00 UTC) and on-demand deployments.
- **Error Handling:** Built-in retry logic and error reporting to handle source fetch failures gracefully.

## How It Works

1. **Fetching Sources:** The script downloads blocklists from multiple URLs.
2. **Normalization:** Rules are processed to convert them into a standardized format. Host file entries are transformed into AdBlock rules.
3. **Filtering:** Whitelisted domains are skipped to avoid blocking essential resources.
4. **Advanced Protections:** Additional security rules are injected.
5. **Optimization:** The blocklist undergoes deduplication, sorting, and wildcard compression.
6. **Output:** The final, optimized blocklist is saved as `robust-blocklist-pro.txt`.

## Repository Structure

- **`robust-blocklist-pro.py`**: The main Python script that generates the blocklist.
- **`.github/workflows/deployment.yml`**: GitHub Actions workflow file that automates the generation and deployment process.
- **`robust-blocklist-pro.txt`**: (Generated) The final blocklist output.

