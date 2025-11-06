import boto3
import os

# Environment variables for flexibility
INSTANCE_ID = os.getenv("INSTANCE_ID", "i-06a368472d073af49")
ALARM_NAME = os.getenv("ALARM_NAME", f"High-CPU-Alarm-{INSTANCE_ID}")
ALARM_DESCRIPTION = os.getenv("ALARM_DESCRIPTION", f"Alarm when CPU exceeds 70% for instance {INSTANCE_ID}")
SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN", "arn:aws:sns:us-east-1:123456789012:EC2-CPU-Alarms")
CPU_THRESHOLD = int(os.getenv("CPU_THRESHOLD", "70"))
PERIOD = int(os.getenv("PERIOD", "300"))
EVALUATION_PERIODS = int(os.getenv("EVALUATION_PERIODS", "2"))

def lambda_handler(event, context):
    cloudwatch = boto3.client('cloudwatch')
    
    try:
        response = cloudwatch.put_metric_alarm(
            AlarmName=ALARM_NAME,
            AlarmDescription=ALARM_DESCRIPTION,
            ActionsEnabled=True,
            AlarmActions=[SNS_TOPIC_ARN],
            MetricName='CPUUtilization',
            Namespace='AWS/EC2',
            Statistic='Average',
            Dimensions=[
                {
                    'Name': 'InstanceId',
                    'Value': INSTANCE_ID
                }
            ],
            Period=PERIOD,
            EvaluationPeriods=EVALUATION_PERIODS,
            Threshold=CPU_THRESHOLD,
            ComparisonOperator='GreaterThanThreshold'
        )
        print(f"Successfully created/updated alarm: {ALARM_NAME}")
        return {"status": "success", "alarm_name": ALARM_NAME}
    
    except Exception as e:
        print(f"Failed to create/update alarm: {e}")
        return {"status": "error", "message": str(e)}
