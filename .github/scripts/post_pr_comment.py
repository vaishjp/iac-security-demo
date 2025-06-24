import os
import requests
import sys

def post_comment(pr_number, comment_body):
    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPOSITORY")

    if not token or not repo:
        print("Missing GITHUB_TOKEN or GITHUB_REPOSITORY environment variables")
        sys.exit(1)

    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    data = {"body": comment_body}

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        print("✅ PR comment posted successfully.")
    else:
        print(f"❌ Failed to post comment. Status: {response.status_code}")
        print(response.text)
        sys.exit(1)

if __name__ == "__main__":
    pr_number = os.getenv("PR_NUMBER")
    if not pr_number:
        print("❌ PR_NUMBER environment variable not found.")
        sys.exit(1)

    try:
        with open("checkov_report.md", "r", encoding="utf-8") as f:
            comment_body = f.read()
    except FileNotFoundError:
        print("❌ Markdown report file not found.")
        sys.exit(1)

    post_comment(pr_number, comment_body)
