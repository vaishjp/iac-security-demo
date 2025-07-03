import json
import sys

# Load the JSON report
with open(sys.argv[1], 'r') as f:
    data = json.load(f)

# Checkov returns a list of result dicts
failed_checks = []

for check in data:
    if check.get("check_result", {}).get("result") == "FAILED":
        failed_checks.append(check)

# Check if any are critical or high severity
block = False
for check in failed_checks:
    severity = check.get("severity", "").lower()
    if severity in ["critical", "high"]:
        block = True
        print(f"❌ Blocking PR due to {severity.upper()} issue in {check.get('file_path')}")

if block:
    sys.exit(1)  # Fail the pipeline
else:
    print("✅ No high or critical issues found.")
