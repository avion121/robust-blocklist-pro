import requests

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

# Download each list and combine them
for url in urls:
    try:
        response = requests.get(url)
        response.raise_for_status()
        content = response.text.strip()
        combined_content.append(content)
    except Exception as e:
        print(f"Error fetching {url}: {e}")

# Append minimal technique rules for Popup Blocker (strict)
technique_rules = """
# Popup Blocker (strict) Techniques
window.open
target=_blank
form submission
""".strip()

combined_content.append(technique_rules)

# Merge everything into one file
final_content = "\n\n".join(combined_content)
with open("combined_list.txt", "w", encoding="utf-8") as f:
    f.write(final_content)

print("combined_list.txt updated.")
