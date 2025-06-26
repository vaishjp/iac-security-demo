import sys
import json
from collections import Counter

def generate_chart(data):
    failed_checks = []

    if isinstance(data, dict):
        failed_checks = data.get("results", {}).get("failed_checks", [])
    elif isinstance(data, list):
        failed_checks = data

    severity_counter = Counter()

    for check in failed_checks:
        severity = check.get("severity")
        if severity and isinstance(severity, str):
            severity_counter[severity.upper()] += 1
        else:
            severity_counter["UNKNOWN"] += 1

    markdown = "# 📊 Severity Summary Chart\n\n"
    markdown += "| Severity | Count |\n"
    markdown += "|----------|-------|\n"
    for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "UNKNOWN"]:
        count = severity_counter.get(severity, 0)
        markdown += f"| {severity} | {count} |\n"

    return markdown

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python severity_summary_chart.py input.json output.md")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        markdown = generate_chart(data)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown)

        print("✅ Severity chart generated successfully.")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
