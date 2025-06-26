import os
import sys
import json
import requests

def send_slack_notification(webhook_url, message):
    payload = {"text": message}
    response = requests.post(webhook_url, json=payload)
    if response.status_code != 200:
        print(f"❌ Slack notification failed: {response.text}")
    else:
        print("✅ Slack notification sent!")

if __name__ == "__main__":
    json_path = sys.argv[1]
    webhook_url = os.environ.get("SLACK_WEBHOOK")

    if not webhook_url:
        print("❌ SLACK_WEBHOOK not set")
        sys.exit(1)

    with open(json_path, "r") as f:
        data = json.load(f)

    failed = data.get("results", {}).get("failed_checks", [])
    critical_or_high = [f for f in failed if f["severity"].upper() in ["CRITICAL", "HIGH"]]

    if critical_or_high:
        send_slack_notification(webhook_url, f"🚨 {len(critical_or_high)} Critical/High issues found in IaC scan!")
    else:
        print("✅ No critical/high issues found. No Slack alert sent.")
