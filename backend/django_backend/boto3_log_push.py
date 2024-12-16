import boto3
import datetime
import os

# Initialize CloudWatch client
client = boto3.client(
    'logs',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
    region_name='us-east-1'
)

# Create log stream (if not exists)
log_group = '/diplomaroad-log-group'
log_stream = 'manual-test-log-stream'

try:
    client.create_log_stream(logGroupName=log_group, logStreamName=log_stream)
except client.exceptions.ResourceAlreadyExistsException:
    pass

# Push log event
timestamp = int(datetime.datetime.now().timestamp() * 1000)
response = client.put_log_events(
    logGroupName=log_group,
    logStreamName=log_stream,
    logEvents=[
        {
            'timestamp': timestamp,
            'message': 'Manual test log to CloudWatch'
        }
    ]
)

print("Manual log push response:", response)
