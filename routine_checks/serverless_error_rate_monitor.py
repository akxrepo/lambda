import boto3
import os

# Environment variables (optional, fallback to defaults)
LAMBDA_FUNCTION_NAME = os.getenv("LAMBDA_FUNCTION_NAME", "aws-notifications")
ALARM_NAME = os.getenv("ALARM_NAME", f"ErrorAlarm-{LAMBDA_FUNCTION_NAME}")
ALARM_DESCRIPTION = os.getenv("ALARM_DESCRIPTION", f"Alarm when the Lambda function {LAMBDA_FUNCTION_NAME} encounters errors")
SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN", "arn:aws:sns:us-east-1:123456789012:LambdaErrorAlarms")

def lambda_handler(event, context):
    cloudwatch = boto3.client('cloudwatch')
    
    try:
        response = cloudwatch.put_metric_alarm(
            AlarmName=ALARM_NAME,
            AlarmDescription=ALARM_DESCRIPTION,
            ActionsEnabled=True,
            AlarmActions=[SNS_TOPIC_ARN],
            MetricName='Errors',
            Namespace='AWS/Lambda',
            Statistic='Sum',
            Dimensions=[
                {
                    'Name': 'FunctionName',
                    'Value': LAMBDA_FUNCTION_NAME
                }
            ],
            Period=300,  # 5 minutes
            EvaluationPeriods=1,
            Threshold=1,
            ComparisonOperator='GreaterThanOrEqualToThreshold'
        )
        print(f"Successfully created/updated alarm: {ALARM_NAME}")
        return {"status": "success", "alarm_name": ALARM_NAME}
    
    except Exception as e:
        print(f"Failed to create/update alarm: {e}")
        return {"status": "error", "message": str(e)}
