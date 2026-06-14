import re

# Update USD/IDR README
usd_readme_path = "../../../HuggingfaceDataset/daily-usd-idr/README.md"
with open(usd_readme_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update num_examples
content = re.sub(r'num_examples: 6168', 'num_examples: 6169', content)
# Update coverage line
content = re.sub(r'Coverage: 6,168 trading days from 2001-06-28 through 2025-12-06',
                 'Coverage: 6,169 trading days from 2001-06-28 through 2025-12-08', content)

with open(usd_readme_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated USD/IDR README.")

# Update IHSG README if needed (no change)
ihsg_readme_path = "../../../HuggingfaceDataset/daily-IHSG/README.md"
with open(ihsg_readme_path, 'r', encoding='utf-8') as f:
    content_ihsg = f.read()

# Check if coverage line needs update (still 2025-12-05)
# No change needed.

with open(ihsg_readme_path, 'w', encoding='utf-8') as f:
    f.write(content_ihsg)

print("IHSG README unchanged.")