# AWS Security Monitoring and Automated Response System

# Comments
02/12 - Upload updated script. 

## Overview
This project demonstrates a cloud-native security monitoring pipeline built in AWS.

The objective is to detect, monitor, and alert on security findings while supporting controlled, analyst-driven response rather than fully automated remediation. This reflects how many real world security teams validate findings before action while using AWS native services in a real-world architecture.

## Architecture
CloudTrail -> GuardDuty -> Security Hub -> EventBridge -> SNS -> Lambda -> s3 + DynamoDB
## Flow Description
- CloudTrail captures API activity.
- GuardDuty analyzes logs and produces security findings.
- Security Hub aggregates findings.
- EventBridge routes qualifying events.
- SNS distributes alert notifications.
- Lambda performs automated response logic:
- Generates unique Case IDs
- Writes structured evidence artifacts to S3
- Stores metadata in DynamoDB
- Publishes notifications

## Work Completed
- Security Hub enabled
- SNS topic created
- EventBridge rule created to forward findings
- Lambda function created for controlled response workflows
- Evidence artificats written to S3
- Case metadata structured and stored
- CloudWatch montioring verified

## Next Steps
- Connect EventBridge to Lambda trigger
- Implement automated remediation logic
- Simulate findings and validate alerts
- Create architecture diagram
  ## Intergration Testing Incident (Unintentional Recursive Invocation)
  
- During integration testing, an S3 trigger was configured on the same bucket used to store evidence artifacts.
When Lambda wrote evidence.json to S3 the PutObject event triggered Lambda again creating a recursive invocation loop.
## Observed Impact

- 438,000 Lambda invocations
- High SNS notification volume
- Throttling observed
- Async retry behavior visible in CloudWatch
- 400k email notifications generated before mitigation
## Root Cause

- S3 event source was not filtered or isolated from the Lambda output bucket.
- Writing to the same bucket that triggers the function created a self-invoking loop.
## Mitigation Actions Taken

- Reserved concurrency set to 0 (immediate halt)
- S3 trigger removed
- SNS subscription deleted
- Metrics monitored until invocation rate dropped to zero
## Key Lessons Learned
- Never write to the same S3 bucket that triggers the Lambda without prefix filtering
- Always isolate ingestion buckets from artifact buckets
- Monitor CloudWatch invocation spikes immediately
- Understand Lambda async retry and event-source behavior
- Implement guardrails before scaling automation
- This experience provided direct exposure to real-world serverless failure modes and recovery strategies.
## Security Design Principles Applied

- Least privilege IAM policies
- Structured case ID generation
- Immutable evidence storage
- Event-driven architecture
- Observability-first debugging
## Next Improvements

- Add CloudWatch alarm for abnormal invocation spikes
- Add severity-based notification filtering
## Author
Larry Jordan  
Cybersecurity / Cloud Security Student



