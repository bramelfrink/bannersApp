import json
import boto3
import os

client = boto3.client('stepfunctions')


def lambda_handler(event, _):
    """
    Trigger the step function whenever a new file is added to the S3 bucket.
    """

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    obj = {
        'bucket': bucket,
        'key': key
    }

    result = json.dumps(obj)

    if 'clicks' in key:
        postfix = 'BannersClickStream-clicks'
    elif 'conversions' in key:
        postfix = 'BannersClickStream-conversions'
    else:
        postfix = 'BannersClickStream-impressions'

    state_machine_arn = 'arn:aws:states:eu-central-1:162258891733:stateMachine:' + postfix

    client.start_execution(
        stateMachineArn=state_machine_arn,
        input=result
    )
