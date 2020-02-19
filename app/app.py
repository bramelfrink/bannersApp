from flask import Flask
import json
import os
import random
from datetime import datetime as dt
from typing import List, Tuple

import boto3
import psycopg2

app = Flask(__name__)

os.environ['CAMPAIGN_BANNERS_TABLE'] = 'serverless-flask-CampaignBanners-TMRSX6KBE5H8'
CAMPAIGN_BANNERS_TABLE = os.environ['CAMPAIGN_BANNERS_TABLE']


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


def get_top_banners(campaign_id: int, time: int) -> int:
    """
    Query RDS revenue table for banners belonging to the campaign.

    :return: a random banner_id from the top 10 banners belonging to the campaign.
    """
    cur = create_cursor()
    query = f"""
    with best as (
    SELECT campaign_id, banner_id, total_revenue, total_clicks, total_impressions
    FROM banners.banner_performance
    WHERE t = {time} and campaign_id = {campaign_id} and total_revenue notnull
    ORDER BY total_revenue DESC, total_clicks DESC, total_impressions DESC
    LIMIT 10
    )
    SELECT *
    FROM best;
    """
    cur.execute(query)
    res: List[Tuple] = cur.fetchall()

    if len(res) == 0:
        raise ValueError('No banners found for this campaign at this time')
    banner = random.choice(res)
    banner_id = banner[1]
    return banner_id


def show_banner(banner_id: int) -> json:
    """
    Generate a URL that points to the S3 bucket in which the banner images are hosted.
    """
    banner_url = f'https://serve-banners.s3.eu-central-1.amazonaws.com/image_{banner_id}.png'
    response = f'<img src="{banner_url}">'
    return response


def get_time() -> int:
    """
    Converts the current time in minutes to 1, 2, 3 or 4.
    This is just for convenience.
    """
    cur_min = dt.now().minute
    if 0 <= cur_min < 15:
        return 1
    elif 15 <= cur_min < 30:
        return 2
    elif 30 <= cur_min < 45:
        return 3
    else:
        return 4


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/campaigns/<int:campaign_id>')
def campaign_page(campaign_id: int):
    """
    Get banners belonging to the campaign_id, based on business rules.
    """
    # query banners based on revenue
    time = get_time()

    try:
        banner_id = get_top_banners(campaign_id, time)
        return show_banner(banner_id)
    except:
        return 'No campaign found'


if __name__ == '__main__':
    app.run()
