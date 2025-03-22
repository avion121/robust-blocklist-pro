# ROBUST-BLOCKLIST-PRO

ROBUST-BLOCKLIST-PRO is a comprehensive aggregated blocklist designed to combine multiple reputable sources into one unified list. This project gathers default filters from popular blocklist providers such as uBlock Origin, EasyList, Online Malicious URL Blocklists, and several other specialized lists.

## Features

- **Aggregated Sources:** Combines blocklists from different categories:
  - **uBlock Origin Default Filters:** filters, badware, privacy, quick-fixes, and unbreak.
  - **EasyList & EasyPrivacy:** Removes ads and trackers.
  - **Online Malicious URL Blocklists:** Includes Feodo Tracker, Ransomware Tracker, and URLhaus.
  - **Peter Lowe's Ad & Tracking Server List**
  - **hagezi Pro Blocklist**
  - **StevenBlack fakenews-gambling Hosts**
  - **OISD Big Full:** Domain blocklist.
  - **1Hosts Lite Adblock List**
  - **Spam404 Main Blacklist**
  - **Malware Host Filter List**
  - **AdGuard Mobile FiltersRegistry**

- **Stealth Techniques:**  
  Uses randomized User-Agent strings, persistent sessions with retry policies, and randomized delays to mimic human browsing.

- **Easy Integration:**  
  Automatically generates an updated blocklist file that can be used with adblockers and other filtering tools.

## How It Works

1. **Scheduled Execution:**  
   A GitHub Actions workflow runs daily at 05:00 UTC (or can be triggered manually) to generate the blocklist.

2. **Python Script:**  
   The script fetches each list from verified URLs, deduplicates them, and aggregates the content with metadata headers.

3. **Commit & Push:**  
   Changes are committed and pushed back to the repository automatically if updates are detected.

## Setup & Deployment

### GitHub Actions Workflow

The workflow file is located at `.github/workflows/deployment.yml`. It sets up the environment, installs dependencies, runs the Python script, and commits the updated blocklist.

### Python Script

The core functionality is implemented in `robust-blocklist-pro.py`. This script:
- Creates a persistent session with retries.
- Fetches each filter list using randomized User-Agent strings.
- Introduces random delays between requests.
- Writes the combined output to `robust-blocklist-pro.txt`.

## Requirements

- Python 3.11 or higher.
- `requests` library (installed automatically by the workflow).

## Contributing

Feel free to fork the repository and suggest improvements or additional sources. Make sure to verify URLs against their official sources before submitting a pull request.

## License

This project is licensed under the MIT License.

---

Copy and paste the above files into your GitHub repository, and the project should run correctly without errors.
