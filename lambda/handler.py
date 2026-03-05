import json
import boto3
from datetime import datetime, timezone


def lambda_handler(event, context):
    """
    Fetches AWS Config compliance results for all rules.
    Returns structured JSON for the dashboard to consume.
    """

    config = boto3.client("config")

    # ── 1. Get all rules and their compliance status ──────────────────────────
    rules_response = config.describe_compliance_by_config_rule()
    rules_compliance = rules_response.get("ComplianceByConfigRules", [])

    # ── 2. Get detailed results per rule (which resources are non-compliant) ──
    results = []

    for rule in rules_compliance:
        rule_name = rule["ConfigRuleName"]
        compliance_type = rule["Compliance"]["ComplianceType"]

        # Fetch non-compliant resources for this rule
        non_compliant_resources = []
        try:
            details = config.get_compliance_details_by_config_rule(
                ConfigRuleName=rule_name,
                ComplianceTypes=["NON_COMPLIANT"],
                Limit=25
            )
            for r in details.get("EvaluationResults", []):
                non_compliant_resources.append({
                    "resourceType": r["EvaluationResultIdentifier"]["EvaluationResultQualifier"]["ResourceType"],
                    "resourceId":   r["EvaluationResultIdentifier"]["EvaluationResultQualifier"]["ResourceId"],
                    "annotation":   r.get("Annotation", "No details provided")
                })
        except Exception:
            pass  # Rule may have no evaluations yet

        results.append({
            "ruleName":              rule_name,
            "complianceType":        compliance_type,         # COMPLIANT | NON_COMPLIANT | NOT_APPLICABLE | INSUFFICIENT_DATA
            "nonCompliantResources": non_compliant_resources,
            "nonCompliantCount":     len(non_compliant_resources)
        })

    # ── 3. Build summary counts ───────────────────────────────────────────────
    summary = {
        "total":              len(results),
        "compliant":          sum(1 for r in results if r["complianceType"] == "COMPLIANT"),
        "nonCompliant":       sum(1 for r in results if r["complianceType"] == "NON_COMPLIANT"),
        "insufficientData":   sum(1 for r in results if r["complianceType"] == "INSUFFICIENT_DATA"),
        "notApplicable":      sum(1 for r in results if r["complianceType"] == "NOT_APPLICABLE"),
        "scannedAt":          datetime.now(timezone.utc).isoformat()
    }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type":                "application/json",
            "Access-Control-Allow-Origin": "*"   # Required for browser → API Gateway calls
        },
        "body": json.dumps({
            "summary": summary,
            "rules":   results
        })
    }
