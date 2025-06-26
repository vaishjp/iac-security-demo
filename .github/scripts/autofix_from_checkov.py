import json
import os

# ✅ Autofix rules for common Checkov issues
FIX_RULES = {
    # Publicly exposed resources (e.g., 0.0.0.0/0) – restrict CIDR
    "CKV_AWS_23": lambda content: content.replace("0.0.0.0/0", "10.0.0.0/16"),

    # S3 bucket without encryption – enable AES256 encryption
    "CKV_AWS_21": lambda content: content.replace(
        'resource "aws_s3_bucket" "',
        'resource "aws_s3_bucket" "\n  server_side_encryption_configuration {\n    rule {\n      apply_server_side_encryption_by_default {\n        sse_algorithm = "AES256"\n      }\n    }\n  }'
    ),

    # Security group rule allows all traffic
    "CKV_AWS_20": lambda content: content.replace("cidr_blocks = [\"0.0.0.0/0\"]", "cidr_blocks = [\"10.0.0.0/16\"]"),
}

def autofix(report_file):
    try:
        with open(report_file, "r") as f:
            report = json.load(f)
    except Exception as e:
        print(f"❌ Failed to load JSON report: {e}")
        return

    if not isinstance(report, list):
        print("❌ Invalid format in report file – expected a list.")
        return

    for issue in report:
        check_id = issue.get("check_id")
        file_path = issue.get("file_path", "").lstrip("/")
        resource = issue.get("resource")

        if not (check_id and file_path and os.path.isfile(file_path)):
            continue

        print(f"🔍 Processing {check_id} in {file_path}...")

        try:
            with open(file_path, "r") as tf:
                original = tf.read()

            if check_id in FIX_RULES:
                fixed = FIX_RULES[check_id](original)

                fixed_path = file_path.replace(".tf", "_fixed.tf")
                with open(fixed_path, "w") as f:
                    f.write(fixed)

                print(f"✅ Fixed file saved: {fixed_path}")
            else:
                print(f"⚠️ No fix rule for {check_id}, skipping.")
        except Exception as e:
            print(f"❌ Error fixing {file_path}: {e}")

if __name__ == "__main__":
    autofix("checkov_report.json")
