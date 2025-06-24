import json
import sys

def parse_checkov_report(json_file):
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"❌ Error loading Checkov JSON report: {e}")
        sys.exit(1)

def generate_markdown(data):
    markdown_lines = ["# 🛡️ Checkov Misconfiguration Report\n"]

    failed_checks = data.get("results", {}).get("failed_checks", [])

    if not failed_checks:
        markdown_lines.append("✅ No misconfigurations found.\n")
    else:
        for check in failed_checks:
            severity = check.get("severity", "UNKNOWN")
            resource = check.get("resource", "UNKNOWN")
            file_path = check.get("file_path", "")
            file_line_range = check.get("file_line_range", [])
            check_id = check.get("check_id", "")
            check_name = check.get("check_name", "")
            guideline = check.get("guideline", "")

            markdown_lines.append(f"### ❗ {check_id} - {check_name}")
            markdown_lines.append(f"- **Severity**: {severity}")
            markdown_lines.append(f"- **Resource**: `{resource}`")
            markdown_lines.append(f"- **File**: `{file_path}` (Lines {file_line_range})")
            if guideline:
                markdown_lines.append(f"- **Guideline**: [Link]({guideline})")
            markdown_lines.append("\n---\n")

    return "\n".join(markdown_lines)

def save_markdown(md_text, output_file):
    try:
        with open(output_file, 'w') as f:
            f.write(md_text)
        print(f"✅ Markdown report generated: {output_file}")
    except Exception as e:
        print(f"❌ Error generating report: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_to_md.py <input_json> <output_md>")
        sys.exit(1)

    json_file = sys.argv[1]
    md_file = sys.argv[2]

    data = parse_checkov_report(json_file)
    md_text = generate_markdown(data)
    save_markdown(md_text, md_file)

    # 🚨 Fail the workflow if there are any high or critical issues
    exit_code = 0
    for check in data.get("results", {}).get("failed_checks", []):
        if check.get("severity", "").lower() in ["high", "critical"]:
            exit_code = 1

    sys.exit(exit_code)
