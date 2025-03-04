import requests
import os

# List of URLs for the 6 blocklists
urls = [
    "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.txt",
    "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling/hosts",
    "https://big.oisd.nl",
    "https://easylist.to/easylist/easylist.txt",
    "https://easylist.to/easylist/easyprivacy.txt",
    "https://raw.githubusercontent.com/badmojr/1Hosts/master/Lite/adblock.txt"
]

combined_content = []

# Download each list and append its raw content (no extra headers)
for url in urls:
    try:
        response = requests.get(url)
        response.raise_for_status()
        content = response.text.strip()
        combined_content.append(content)
    except Exception as e:
        print(f"Error fetching {url}: {e}")

# Append all Popup Blocker (strict) technique commands (actionable rules only)
popup_techniques = """
window.open
target=_blank
form submission
Deny popup request
Allow popup request
Open popup request in a background tab
Redirect current page to popup URL source
""".strip()

combined_content.append(popup_techniques)

# Merge all content into one string
final_content = "\n\n".join(combined_content)

# Define output file name
output_file = "robust-blocklist-pro.txt"

# Remove old files if they exist
if os.path.exists("combined_list.txt"):
    os.remove("combined_list.txt")
if os.path.exists(output_file):
    os.remove(output_file)

# Write the new content to robust-blocklist-pro.txt
with open(output_file, "w", encoding="utf-8") as f:
    f.write(final_content)

print(f"{output_file} updated.")
