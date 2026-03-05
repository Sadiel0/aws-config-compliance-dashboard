# AWS Setup Guide

## Prerequisites
- AWS account with console access
- AWS Config enabled (Step 1 — already done)

---

## Step 2: Lambda Function

1. Go to **Lambda → Create function**
   - Name: `config-compliance-fetcher`
   - Runtime: Python 3.12
   - Execution role: Create new role with basic Lambda permissions
   - Click **Create function**

2. Paste the contents of `lambda/handler.py` into the inline code editor

3. Click **Deploy**

---

## Step 3: IAM Permissions for Lambda

Your Lambda's execution role needs permission to read AWS Config data.

1. Go to **IAM → Roles** → search for `config-compliance-fetcher`
2. Click the role → **Add permissions → Attach policies**
3. Search and attach: **`AWS_ConfigRole`** (AWS managed policy)
   - Or create an inline policy with just these actions:
     ```json
     {
       "Effect": "Allow",
       "Action": [
         "config:DescribeComplianceByConfigRule",
         "config:GetComplianceDetailsByConfigRule"
       ],
       "Resource": "*"
     }
     ```

4. **Test your Lambda** — hit the **Test** button with any JSON payload `{}`. You should see compliance data returned.

---

## Step 4: API Gateway

1. Go to **API Gateway → Create API → HTTP API**
   - Name: `config-dashboard-api`
   - Click **Next**

2. Add integration:
   - Integration type: Lambda
   - Lambda function: `config-compliance-fetcher`
   - Click **Next**

3. Configure route:
   - Method: `GET`
   - Resource path: `/compliance`
   - Click **Next → Next → Create**

4. Copy your **Invoke URL** (looks like `https://abc123.execute-api.us-east-1.amazonaws.com`)

5. Open `dashboard/index.html` and replace `YOUR_API_GATEWAY_URL` with your Invoke URL + `/compliance`

---

## Step 5: Open the Dashboard

Open `dashboard/index.html` directly in your browser. It will call your live API and display real compliance data from your AWS account.

---

## Cleanup (avoid ongoing charges)

To avoid charges after you're done:
- **Lambda**: No cost unless invoked
- **API Gateway**: ~$1/million requests (basically free)
- **AWS Config**: ~$0.003 per configuration item recorded — **disable rules you don't need**
  - Config → Rules → select rule → Actions → Delete
