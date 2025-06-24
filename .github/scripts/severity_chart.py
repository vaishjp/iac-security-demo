import json
import matplotlib.pyplot as plt
from collections import Counter

def generate_severity_chart(json_path, output_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        failed_checks = data
    else:
        failed_checks = data.get("results", {}).get("failed_checks", [])

    severities = Counter(check.get("severity", "UNKNOWN") for check in failed_checks)
    levels = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "UNKNOWN"]
    counts = [severities.get(level, 0) for level in levels]

    # Plot
    plt.figure(figsize=(8, 5))
    bars = plt.bar(levels, counts, color=['#e74c3c', '#e67e22', '#f1c40f', '#3498db', '#95a5a6'])
    plt.title("Checkov Misconfiguration Severity Count")
    plt.xlabel("Severity")
    plt.ylabel("Count")
    for bar, count in zip(bars, counts):
        plt.text(bar.get_x() + bar.get_width()/2.0, bar.get_height(), str(count), ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(output_path)
    print(f"✅ Chart saved as {output_path}")

if __name__ == "__main__":
    generate_severity_chart("checkov_report.json", "severity_chart.png")
