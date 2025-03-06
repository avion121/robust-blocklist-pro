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

# Download each list and process its content
for url in urls:
    try:
        response = requests.get(url)
        response.raise_for_status()
        content = response.text.strip()
        # Replace "HaGeZi's Pro DNS Blocklist" with "robust-blocklist-pro"
        content = content.replace("HaGeZi's Pro DNS Blocklist", "robust-blocklist-pro")
        combined_content.append(content)
    except Exception as e:
        print(f"Error fetching {url}: {e}")

# Add a comprehensive rule to block any popup redirects permanently.
# This rule uses a regular expression to match any URL containing the words "popup" and "redirect"
# in sequence (ignoring case) and applies the "$popup" option to ensure it's enforced.
popup_rule = "/popup.*redirect/i$popup"
combined_content.append(popup_rule)

# Merge all content into one string with proper separation
final_content = "\n\n".join(combined_content)

# Define output file name
output_file = "robust-blocklist-pro.txt"

# Remove old files if they exist
if os.path.exists("combined_list.txt"):
    os.remove("combined_list.txt")
if os.path.exists(output_file):
    os.remove(output_file)

# Write the final content to the output file
with open(output_file, "w", encoding="utf-8") as f:
    f.write(final_content)

print(f"{output_file} updated.")
