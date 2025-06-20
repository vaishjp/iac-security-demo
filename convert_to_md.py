import json

with open("checkov_report.json", "r") as f:
    data = json.load(f)

markdown = "# ✅ Checkov Security Report\n\n"

failed_checks = data.get("results", {}).get("failed_checks", [])

if not failed_checks:
    markdown += "🎉 No failed checks! Your code is safe.\n"
else:
    for check in failed_checks:
        markdown += f"## ❌ {check['check_id']} - {check['check_name']}\n"
        markdown += f"- **File:** `{check['file_path']}`\n"
        markdown += f"- **Resource:** `{check['resource']}`\n"
        markdown += f"- **Severity:** {check['severity']}`\n\n"

with open("checkov_report.md", "w") as f:
    f.write(markdown)
