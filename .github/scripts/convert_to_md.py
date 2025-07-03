import json
import sys
from datetime import datetime
from collections import Counter

def generate_markdown(data):
    failed_checks = data.get("results", {}).get("failed_checks", [])
    
    if not failed_checks:
        return "# ✅ No Misconfigurations Found\nGreat job! 🎉"

    severities = Counter(check.get("severity", "UNKNOWN") for check in failed_checks)

    md = "# 🛡️ Checkov Misconfiguration Report\n\n"
    md += f"🕒 **Scan Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

    md += "## 📊 Summary\n"
    for level in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "UNKNOWN"]:
        if level in severities:
            md += f"- {level}: {severities[level]}\n"
    md += "\n---\n"

    for check in failed_checks:
        severity = check.get("severity", "UNKNOWN")
        resource = check.get("resource", "UNKNOWN")
        file_path = check.get("file_path", "")
        check_id = check.get("check_id", "")
        check_name = check.get("check_name", "")
        guideline = check.get("guideline", "")
        line_range = check.get("file_line_range", [])

        md += f"### ❗ {check_id} - {check_name}\n"
        md += f"- **Severity**: {severity}\n"
        md += f"- **Resource**: `{resource}`\n"
        md += f"- **File**: `{file_path}` (Lines {line_range})\n"
        if guideline:
            md += f"- **Guideline**: [Link]({guideline})\n"
        md += "\n---\n"

    return md

if __name__ == "__main__":
    try:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            data = json.load(f)
        
        if isinstance(data, list):  # Fix if raw list
            data = {"results": {"failed_checks": data}}

        markdown = generate_markdown(data)
        with open(sys.argv[2], "w", encoding="utf-8") as f:
            f.write(markdown)

        print("✅ Markdown report generated.")
    except Exception as e:
        print(f"❌ Error generating report: {e}")
