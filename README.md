# AWS Config Compliance Dashboard

A real-time AWS compliance monitoring dashboard powered by AWS Config, Lambda, and API Gateway. Paste any IAM policy or point it at your live account to surface misconfigurations by severity.

![Architecture](https://img.shields.io/badge/AWS-Config%20%7C%20Lambda%20%7C%20API%20Gateway-orange?style=flat-square&logo=amazon-aws)
![Language](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)
![Frontend](https://img.shields.io/badge/Frontend-Vanilla%20HTML%2FJS-green?style=flat-square)

---

## What It Does

- Queries live AWS Config compliance data across all enabled rules
- Shows per-rule compliance status: COMPLIANT / NON-COMPLIANT / INSUFFICIENT DATA
- Drills down into which specific resources are violating each rule
- Displays a real-time compliance score (0–100%)
- Zero dependencies — single HTML file frontend, no framework needed

## Architecture

```
AWS Config Rules
      │
      ▼
Lambda (Python) ──── boto3 ──── config:DescribeComplianceByConfigRule
      │                          config:GetComplianceDetailsByConfigRule
      ▼
API Gateway (HTTP API)
      │
      ▼
Dashboard (index.html) ──── fetch() ──── Live compliance data
```

## Config Rules Monitored

| Rule | What It Checks |
|------|---------------|
| `s3-bucket-public-read-prohibited` | S3 buckets should not allow public read access |
| `iam-root-access-key-check` | Root account should not have active access keys |
| `iam-password-policy` | IAM password policy meets complexity requirements |
| `restricted-ssh` | Security groups should not allow unrestricted SSH (port 22) |
| `ec2-imdsv2-check` | EC2 instances should require IMDSv2 |

## Setup

See [`infrastructure/setup.md`](infrastructure/setup.md) for full step-by-step instructions.

**Quick start:**
1. Enable AWS Config + add managed rules (see setup guide)
2. Deploy `lambda/handler.py` as a Lambda function
3. Attach Config read permissions to Lambda execution role
4. Create HTTP API Gateway pointing to Lambda
5. Open `dashboard/index.html`, paste your API URL, hit Scan

## Skills Demonstrated

- AWS Config managed rules and compliance evaluation
- Lambda function design with least-privilege IAM
- API Gateway HTTP API + CORS configuration
- Serverless architecture patterns
- Real-time dashboard with live AWS data

## Author

**Sadiel Almanza** · [GitHub](https://github.com/Sadiel0) · [LinkedIn](https://linkedin.com/in/sadielalmanza/) · [Portfolio](https://stalwart-entremet-86e74e.netlify.app)
