ROBUST-BLOCKLIST-PRO

ROBUST-BLOCKLIST-PRO is an advanced blocklist generator that aggregates trusted blocklists from multiple sources and consolidates them into one comprehensive, optimized blocklist. It fetches data from a curated list of reliable feeds, automatically removes duplicate sources, and produces a unified output file. Updates are fully automated via GitHub Actions, ensuring your blocklist remains current with daily deployments at 05:00 UTC.

GitHub Actions Status


Table of Contents
Features
How It Works
Repository Structure
Installation
Usage
Configuration
Contributing
License
Features
Aggregated Trusted Sources:
Consolidates blocklists from multiple reliable feeds (including uBlock Origin filters, EasyList, Peter Lowe’s list, and additional protection and threat intelligence sources).

Automated Updates:
Uses a GitHub Actions workflow to fetch, combine, and deploy the blocklist daily at 05:00 UTC (or via manual dispatch).

Deduplication:
Automatically removes duplicate URLs, ensuring each unique source is processed only once.

Robust Error Handling:
Incorporates retry logic and error reporting for dependable source fetching.

Comprehensive Coverage:
Combines a wide range of lists to maximize blocking of unwanted content while preserving legitimate websites.

How It Works
Fetching Sources:
The generator downloads blocklists from multiple trusted URLs using a retry-enabled HTTP session.

Deduplication:
Duplicate URLs are automatically removed while preserving the original order.

Aggregation:
The contents of all fetched lists are combined into a single file with metadata annotations, including the source URL for each section.

Output Generation:
The final consolidated blocklist is written to robust-blocklist-pro.txt.

Automated Deployment:
A GitHub Actions workflow runs daily (or via manual dispatch) to update and commit the new blocklist automatically.

Repository Structure
robust-blocklist-pro.py
The main Python script that aggregates, deduplicates, and generates the consolidated blocklist.

.github/workflows/robust-blocklist-pro.yml
The GitHub Actions workflow file for automated generation and deployment of the blocklist.

robust-blocklist-pro.txt
(Generated) The final, consolidated blocklist output file.

Installation
Clone the Repository:

bash
Copy
Edit
git clone https://github.com/your-username/your-repository.git
cd your-repository
(Optional) Set Up a Virtual Environment and Install Dependencies:

bash
Copy
Edit
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install requests
Usage
Manual Execution:
Run the generator script locally:

bash
Copy
Edit
python robust-blocklist-pro.py
This command fetches and combines the blocklists, writing the output to robust-blocklist-pro.txt.

Automated Updates:
The GitHub Actions workflow (located at .github/workflows/robust-blocklist-pro.yml) runs daily at 05:00 UTC (or can be triggered manually) to update and commit the new blocklist automatically.

Configuration
The list of source URLs is defined within robust-blocklist-pro.py. You can add or remove URLs as needed.
The script employs retry logic for robustness; you can modify the timeout or retry parameters directly in the script.
To further customize, update the metadata header within the script.
Contributing
Contributions are welcome! Please fork the repository and submit pull requests for any improvements or bug fixes. Follow the repository’s coding standards and include appropriate tests.

License
This project is licensed under the MIT License.
