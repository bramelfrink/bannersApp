"""
Read input data from S3, remove duplicate rows, remove rows that are already in DynamoDB and write to S3.
"""
from functions.deduplicate.src.deduplicate import deduplicate_input, DynamoDBDeduplication, find_duplicates
from helpers.s3 import S3


def deduplicate(event, name: str):
    """
    Deduplicates the input files and checks if the id is already present in DynamoDB
    """
    # read from S3
    s3 = S3(event['bucket'], event['key'], 'deduplicated')
    df = s3.read()

    # deduplicate input
    df_partially_deduplicated = deduplicate_input(df, 'click_id')

    # deduplicate using DynamoDB
    dynamodb = DynamoDBDeduplication('click_id')
    deduplicated_df = df_partially_deduplicated[df_partially_deduplicated['click_id'].apply(dynamodb.is_unique)]

    # store full records in DynamoDB

    # find and store duplicates
    # Only stores completely dropped columns, because duplicates within the same CSV file are already dropped by
    # deduplicate_input().
    # I did it this way to make less call to DynamoDB.
    duplicate_df = find_duplicates(df, deduplicated_df)
    s3.write(duplicate_df, f'duplicates/{name}/')

    # write to S3
    s3.write(deduplicated_df, s3.folder_write)


def click_lambda_handler(event, _):
    """Deduplicates click events"""
    deduplicate(event, 'clicks')


def conversion_lambda_handler(event, _):
    """Deduplicates conversion events"""
    deduplicate(event, 'conversions')
