#!/usr/bin/env python3
import re

# Read file
with open('generate_report_fixed.py', 'r') as f:
    content = f.read()

# Add target="_blank" to tweet links
old_pattern = r"<a href=\"{x_url}\">View on X</a>"
new_text = '<a href="{x_url}" target="_blank">View on X</a>'

content = re.sub(old_pattern, new_text, content)

with open('generate_report_fixed.py', 'w') as f:
    f.write(content)

print("Added target=_blank to View on X links")
