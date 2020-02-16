"""
Read input data from S3, remove duplicate rows, remove rows that are already in DynamoDB and write to S3.
"""
from helpers.s3 import S3
from functions.deduplicate.src.deduplicate import deduplicate_input


def lambda_handler(event, context):
    """
    The handler is called whenever the Lambda function is invoked.

    :param event:
    :param context:
    :return:
    """
    # read from S3
    s3 = S3(event['bucket'], event['key'], 'deduplicated')
    df = s3.read()

    # deduplicate input
    df = deduplicate_input(df, 'click_id')

    # deduplicate using DynamoDB

    # write to S3
    s3.write(df)
