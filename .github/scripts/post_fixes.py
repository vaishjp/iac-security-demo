import json
import sys
import os
import requests

def extract_fixes(data):
    failed_checks = data.get("results", {}).get("failed_checks", [])
    suggestions = []

    for check in failed_checks:
        resource = check.get("resource")
        file_path = check.get("file_path")
        check_id = check.get("check_id")
        guideline = check.get("guideline", "No guideline provided.")
        check_name = check.get("check_name")

        fix_tip = f"❗ **{check_id} - {check_name}**\n"
        fix_tip += f"- **File:** `{file_path}`\n"
        fix_tip += f"- **Resource:** `{resource}`\n"
        fix_tip += f"- **Suggestion:** {guideline}\n"
        fix_tip += "---\n"
        suggestions.append(fix_tip)

    return "\n".join(suggestions) if suggestions else "✅ No failed checks to fix!"

def post_comment(pr_number, body, repo, token):
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = { "body": body }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        print("✅ Fix suggestion comment posted.")
    else:
        print(f"❌ Failed to post comment: {response.status_code}\n{response.text}")

if __name__ == "__main__":
    with open("checkov_report.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    suggestion_comment = "## 🔧 Fix Suggestions for IaC Issues\n" + extract_fixes(data)

    github_repo = os.environ.get("GITHUB_REPOSITORY")
    pr_number = os.environ.get("PR_NUMBER")
    github_token = os.environ.get("GITHUB_TOKEN")

    if not all([github_repo, pr_number, github_token]):
        print("❌ Missing environment variables")
        sys.exit(1)

    post_comment(pr_number, suggestion_comment, github_repo, github_token)
