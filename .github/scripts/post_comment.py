import os
import requests
import sys

def post_comment(pr_number, body, repo, token):
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "body": body
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        print("✅ Comment posted successfully!")
    else:
        print(f"❌ Failed to post comment: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        comment_body = f.read()

    github_repo = os.environ.get("GITHUB_REPOSITORY")
    pr_number = os.environ.get("PR_NUMBER")
    github_token = os.environ.get("GITHUB_TOKEN")

    if not (github_repo and pr_number and github_token):
        print("❌ Missing environment variables")
        sys.exit(1)

    post_comment(pr_number, comment_body, github_repo, github_token)
