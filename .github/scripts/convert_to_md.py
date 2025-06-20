'''
import os
import json

# Check if JSON file exists
if not os.path.exists("checkov_report.json"):
    print("❌ checkov_report.json not found. Cannot convert.")
    exit(1)

# Try to load the file
with open("checkov_report.json", "r") as f:
    try:
        data = json.load(f)
    except json.JSONDecodeError:
        print("❌ JSON file is invalid or empty.")
        exit(1)

# Continue with conversion logic here...
# Generate a Markdown table or summary report and save it as checkov_report.md
'''
'''
import json
import os
import sys

# Step 1: Load Checkov report
if not os.path.exists("checkov_report.json"):
    print("❌ checkov_report.json not found.")
    sys.exit(1)

with open("checkov_report.json", "r") as f:
    try:
        data = json.load(f)
    except json.JSONDecodeError:
        print("❌ Invalid JSON format.")
        sys.exit(1)

# Step 2: Prepare markdown
markdown = "# 🛡 Checkov Scan Report\n\n"
markdown += "| Check ID | Severity | Resource | File |\n"
markdown += "|----------|----------|----------|------|\n"

high_or_critical_count = 0

for result in data.get("results", {}).get("failed_checks", []):
    check_id = result.get("check_id", "")
    severity = result.get("severity", "")
    resource = result.get("resource", "")
    file_path = result.get("file_path", "")
    
    if severity.lower() in ["high", "critical"]:
        high_or_critical_count += 1

    markdown += f"| {check_id} | {severity} | {resource} | {file_path} |\n"

with open("checkov_report.md", "w") as f:
    f.write(markdown)

print("✅ Markdown report generated.")

# Step 3: Block PR if high/critical issues exist
if high_or_critical_count > 0:
    print(f"❌ Found {high_or_critical_count} high/critical issues.")
    sys.exit(1)  # Fail pipeline
else:
    print("✅ No high/critical issues found.")
    sys.exit(0)
'''
"""
import json
import sys

# Load the Checkov JSON output
try:
    with open("checkov_report.json") as f:
        checkov_results = json.load(f)
except FileNotFoundError:
    print("❌ checkov_report.json not found.")
    sys.exit(1)

# Load the custom misconfiguration descriptions
try:
    with open(".iac-misconfigs.json") as f:
        misconfigs = json.load(f)
except FileNotFoundError:
    print("❌ .iac-misconfigs.json not found.")
    sys.exit(1)

# Map resources to descriptions
desc_lookup = {item["resource"]: item for item in misconfigs}

# Start building the Markdown report
report_lines = [
    "# ✅ IaC Security Report by Checkov",
    "",
    "| Check ID | Severity | Resource | File | Description |",
    "|----------|----------|----------|------|-------------|"
]

exit_code = 0  # Will be set to 1 if any high/critical issue found

for result in checkov_results.get("results", {}).get("failed_checks", []):
    check_id = result.get("check_id", "N/A")
    severity = result.get("severity", "N/A")
    resource = result.get("resource", "N/A")
    file_path = result.get("file_path", "N/A").replace("./", "")
    resource_type = result.get("resource_type", "")

    # Look up a human-friendly description from dataset
    match = desc_lookup.get(resource_type, {})
    description = match.get("description", "See Checkov docs")

    report_lines.append(f"| {check_id} | {severity} | {resource} | {file_path} | {description} |")

    # Exit with failure if high/critical issue found
    if severity.upper() in ["HIGH", "CRITICAL"]:
        exit_code = 1

# Write the Markdown report
with open("checkov_report.md", "w") as f:
    f.write("\n".join(report_lines))

print("✅ Markdown report generated: checkov_report.md")

# Exit appropriately
sys.exit(exit_code)
"""


name: IaC Security Check

on:
  push:
    branches:
      - test-checkov
  pull_request:
    branches:
      - main

jobs:
  checkov_scan:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install Checkov
        run: pip install checkov

      - name: Run Checkov scan
        run: checkov -d . --output json > checkov_report.json

      - name: Convert Checkov JSON to Markdown
        run: python .github/scripts/convert_to_md.py

      - name: Upload Markdown Report
        uses: actions/upload-artifact@v4
        with:
          name: checkov_markdown_report
          path: checkov_report.md
