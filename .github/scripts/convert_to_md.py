import json
import sys

def generate_markdown(data):
    md = "# 🛡️ Checkov Misconfiguration Report\n\n"
    for check in data:
        if check.get("check_result", {}).get("result") != "FAILED":
            continue
        severity = check.get("severity", "UNKNOWN")
        resource = check.get("resource", "UNKNOWN")
        file_path = check.get("file_path", "")
        file_line_range = check.get("file_line_range", [])
        check_id = check.get("check_id", "")
        check_name = check.get("check_name", "")
        
        md += f"### ❗ {check_id} - {check_name}\n"
        md += f"- **Severity**: {severity}\n"
        md += f"- **Resource**: `{resource}`\n"
        md += f"- **File**: `{file_path}` (Lines {file_line_range})\n"
        md += "\n---\n"
    return md

if __name__ == "__main__":
    try:
        with open(sys.argv[1], 'r') as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("Expected a list of checks in JSON output")
        md_text = generate_markdown(data)
        with open(sys.argv[2], 'w') as f:
            f.write(md_text)
        print("✅ Markdown report generated successfully.")
    except Exception as e:
        print(f"❌ Error generating report: {e}")
        sys.exit(1)
