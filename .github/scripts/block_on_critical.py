import json
import sys

with open(sys.argv[1], "r") as f:
    data = json.load(f)

failed_checks = data.get("results", {}).get("failed_checks", [])
fail = False

for check in failed_checks:
    severity = check.get("severity", "").lower()
    if severity in ["high", "critical"]:
        print(f"❌ Found high/critical issue: {check.get('check_id')} - Severity: {severity}")
        fail = True

if fail:
    sys.exit(1)  # fail the workflow
else:
    print("✅ No high/critical issues found.")
