import json
import boto3
import os
from datetime import datetime

sns = boto3.client("sns")
ec2 = boto3.client("ec2")

SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN")
SEVERITY_THRESHOLD = float(os.environ.get("SEVERITY_THRESHOLD", 7.0))


def lambda_handler(event, context):
    print("Received event:")
    print(json.dumps(event, indent=2))

    findings = event.get("detail", {}).get("findings", [])

    for finding in findings:
        process_finding(finding)

    return {
        "statusCode": 200,
        "body": "Findings processed successfully"
    }


def process_finding(finding):
    title = finding.get("Title")
    severity = finding.get("Severity", {}).get("Label")
    numeric_severity = finding.get("Severity", {}).get("Normalized", 0) / 10
    resource = finding.get("Resources", [{}])[0].get("Id", "Unknown")
    account_id = finding.get("AwsAccountId")

    print(f"[{datetime.utcnow()}] Processing finding: {title}")
    print(f"Severity: {severity} | Score: {numeric_severity}")

    message = f"""
Security Hub Finding Detected

Title: {title}
Severity: {severity}
Score: {numeric_severity}
Resource: {resource}
Account: {account_id}
"""

    # Send SNS Alert
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=f"Security Alert: {title}",
        Message=message
    )

    # Controlled remediation logic
    if numeric_severity >= SEVERITY_THRESHOLD:
        print("High severity detected. Executing controlled remediation...")
        remediate(resource)
    else:
        print("Severity below threshold. Analyst review required.")


def remediate(resource_id):
    """
    Example remediation: Stop EC2 instance
    Only runs if severity >= threshold
    """

    if resource_id.startswith("arn:aws:ec2"):
        instance_id = resource_id.split("/")[-1]
        try:
            ec2.stop_instances(InstanceIds=[instance_id])
            print(f"EC2 instance {instance_id} stopped successfully.")
        except Exception as e:
            print(f"Remediation failed: {str(e)}")
    else:
        print("No automated remediation configured for this resource.")

