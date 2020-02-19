"""
Store the deduplicated, raw, events in RDS MySql.
"""
import json

import boto3
import psycopg2
from pandas import DataFrame

from helpers.s3 import S3


def add_time(df: DataFrame, filename: str):
    print(filename)
    time = filename.split('_')[1]
    df['time'] = time


def create_cursor():
    """
    Creates cursor to the database.
    """
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(
        SecretId='postgres_db'
    )
    secret_string = json.loads(response['SecretString'])

    conn = psycopg2.connect(dbname='postgres',
                            host=secret_string['host'], port=secret_string['port'],
                            user=secret_string['username'], password=secret_string['password'])
    conn.autocommit = True

    return conn.cursor()


def read_data(event) -> DataFrame:
    # read from S3
    s3 = S3(event['bucket'], event['key'], '_')
    df = s3.read()

    # add time column
    add_time(df, event['key'])

    return df


def clicks_lambda_handler(event, _):
    """
    Store data
    """
    df = read_data(event)

    cur = create_cursor()

    # Insert into Postgres
    for _, row in df.iterrows():
        query = f"""
                INSERT INTO banners.clicks VALUES ({row['click_id']}, {row['banner_id']}, {row['campaign_id']}, {row['time']});
                """
        cur.execute(query)


def conversions_lambda_handler(event, _):
    """
    Store data
    """
    df = read_data(event)

    cur = create_cursor()

    # Insert into Postgres
    for _, row in df.iterrows():
        query = f"""
                INSERT INTO banners.conversions VALUES ({row['conversion_id']}, {row['click_id']}, {row['revenue']}, {row['time']});
                """
        cur.execute(query)


def impressions_lambda_handler(event, _):
    """
    Store data
    """
    df = read_data(event)

    cur = create_cursor()

    # Insert into Postgres
    for _, row in df.iterrows():
        query = f"""
                INSERT INTO banners.clicks VALUES ({row['banner_id']}, {row['campaign_id']}, {row['time']});
                """
        cur.execute(query)
