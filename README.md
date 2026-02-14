# AWS Security Monitoring and Automated Response System

## Overview
This project demonstrates a cloud-native security monitoring pipeline built in AWS.

The objective is to detect, monitor, and respond to security findings using AWS native services in a real-world architecture.

## Architecture
CloudTrail → GuardDuty → Security Hub → EventBridge → SNS → Lambda

## Work Completed
- Security Hub enabled
- SNS topic created
- EventBridge rule created to forward findings
- Lambda function created for automated response

## Next Steps
- Connect EventBridge to Lambda trigger
- Implement automated remediation logic
- Simulate findings and validate alerts
- Create architecture diagram

## Author
Larry Jordan  
Cybersecurity / Cloud Security Student



