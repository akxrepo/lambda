import boto3
import os

# Get retention days from environment variable (default: 365)
RETENTION_DAYS = int(os.getenv("RETENTION_DAYS", "365"))

def lambda_handler(event, context):
    logs_client = boto3.client('logs')
    updated = 0
    failed = 0

    print(f"Setting CloudWatch log retention to {RETENTION_DAYS} days...")

    paginator = logs_client.get_paginator('describe_log_groups')

    for page in paginator.paginate():
        for log_group in page.get('logGroups', []):
            name = log_group['logGroupName']
            retention = log_group.get('retentionInDays')

            # Only update if retention not already set
            if retention is None or retention != RETENTION_DAYS:
                try:
                    logs_client.put_retention_policy(
                        logGroupName=name,
                        retentionInDays=RETENTION_DAYS
                    )
                    updated += 1
                    print(f"Updated retention for {name}")
                except Exception as e:
                    failed += 1
                    print(f"Failed to update {name}: {e}")

    print(f"Completed. Updated: {updated}, Failed: {failed}")
    return {"updated": updated, "failed": failed}
