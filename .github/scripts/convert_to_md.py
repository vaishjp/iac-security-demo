import json
import sys

def load_checkov_output(json_file_path):
    with open(json_file_path, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error: {e}")
            sys.exit(1)

def format_check(check):
    severity = check.get('severity', 'UNKNOWN')
    resource = check.get('resource', 'UNKNOWN')
    check_id = check.get('check_id', '')
    check_name = check.get('check_name', '')
    file_path = check.get('file_path', '')
    file_line_range = check.get('file_line_range', [])

    return f"""### ❗ {check_id} - {check_name}
- **Severity**: {severity}
- **Resource**: `{resource}`
- **File**: `{file_path}` (Lines {file_line_range})
"""

def generate_markdown_report(checks, output_path):
    with open(output_path, 'w') as f:
        f.write("# 🛡️ Checkov Misconfiguration Report\n\n")
        if not checks:
            f.write("✅ No misconfigurations found!\n")
        else:
            for check in checks:
                f.write(format_check(check))
                f.write("\n---\n")

def main():
    if len(sys.argv) != 3:
        print("Usage: python convert_to_md.py <input_json> <output_md>")
        sys.exit(1)

    input_json = sys.argv[1]
    output_md = sys.argv[2]

    try:
        data = load_checkov_output(input_json)

        # Handle different formats
        if isinstance(data, dict) and "results" in data:
            checks = data["results"].get("failed_checks", [])
        elif isinstance(data, list):
            checks = data
        else:
            print("❌ Error: Unexpected Checkov output format.")
            sys.exit(1)

        generate_markdown_report(checks, output_md)
        print(f"✅ Markdown report generated: {output_md}")
    except Exception as e:
        print(f"❌ Error generating report: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
