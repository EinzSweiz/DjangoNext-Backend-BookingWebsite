import logging
import watchtower
from django.http import JsonResponse
import boto3

def test_logging(request):
    logger = logging.getLogger('django_watchtower_test')
    logger.setLevel(logging.DEBUG)

    handler = watchtower.CloudWatchLogHandler(
        log_group='/diplomaroad-log-group',
        stream_name='manual-test-log-stream',
        boto3_client=boto3.client(
            'logs',
            aws_access_key_id='your_access_key',
            aws_secret_access_key='your_secret_key',
            region_name='us-east-1'
        )
    )
    logger.addHandler(handler)

    logger.debug("Testing logging from Django!")
    return JsonResponse({'message': 'Logged to CloudWatch!'})
