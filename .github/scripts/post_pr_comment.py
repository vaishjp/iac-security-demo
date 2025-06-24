import os
import requests

# Get inputs from environment
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")
GITHUB_PR_NUMBER = os.getenv("PR_NUMBER")

if not GITHUB_PR_NUMBER:
    print("❌ Error: PR_NUMBER not set.")
    exit(1)

# Read the markdown report
with open("checkov_report.md", "r", encoding="utf-8") as file:
    comment_body = file.read()

# Prepare the API call
url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/issues/{GITHUB_PR_NUMBER}/comments"
headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}
data = {
    "body": comment_body
}

# Make the API call
response = requests.post(url, headers=headers, json=data)

if response.status_code == 201:
    print("✅ Comment posted successfully.")
else:
    print(f"❌ Failed to post comment: {response.status_code}\n{response.text}")
    exit(1)
