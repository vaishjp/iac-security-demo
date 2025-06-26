import json
import sys
import os
import shutil
import re

FIX_RULES = {
    # Example rule: Fix public EC2 instances
    "CKV_AWS_88": {
        "pattern": r'(resource\s+"aws_instance"\s+".*?"\s*\{[\s\S]*?)associate_public_ip_address\s+=\s+true',
        "fix": r'\1associate_public_ip_address = false',
        "note": "Removed public IP assignment from EC2"
    },
    # Add more rules below...
    "CKV_AWS_20": {
        "pattern": r'acl\s+=\s+"public-read"',
        "fix": r'acl = "private"',
        "note": "Set S3 bucket ACL to private"
    }
}

def load_failed_checks(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    # Ensure we’re dealing with a list
    if isinstance(data, list):
        return data
    return data.get("results", {}).get("failed_checks", [])

def apply_fix_to_file(file_path, check_id):
    rule = FIX_RULES.get(check_id)
    if not rule or not os.path.exists(file_path):
        return None

    with open(file_path, "r") as f:
        content = f.read()

    new_content = re.sub(rule["pattern"], rule["fix"], content, flags=re.MULTILINE)

    fixed_file_path = file_path.replace(".tf", "_fixed.tf")
    with open(fixed_file_path, "w") as f:
        f.write(new_content)

    return fixed_file_path

def main(report_path):
    fixes_made = []

    checks = load_failed_checks(report_path)
    for check in checks:
        check_id = check["check_id"]
        file_path = check["file_path"].lstrip("./")
        fixed_file = apply_fix_to_file(file_path, check_id)
        if fixed_file:
            fixes_made.append(f"✅ {check_id} fixed in {fixed_file}")

    if not fixes_made:
        print("❌ No auto-fixes applied (no matching rules or no changes needed)")
    else:
        print("\n".join(fixes_made))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python autofix_from_checkov.py checkov_report.json")
        sys.exit(1)
    main(sys.argv[1])
