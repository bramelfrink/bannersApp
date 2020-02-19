import json
import os
from datetime import datetime as dt

import boto3

from flask import Flask, jsonify, request

app = Flask(__name__)

os.environ['CAMPAIGN_BANNERS_TABLE'] = 'serverless-flask-CampaignBanners-TMRSX6KBE5H8'
CAMPAIGN_BANNERS_TABLE = os.environ['CAMPAIGN_BANNERS_TABLE']
client = boto3.client('dynamodb')


@app.route('/')
def hello_world():
    return 'Hello World!'


def get_top_banners(campaign_id: int, time: int) -> str:
    """
    Query RDS revenue table for banners belonging to the campaign.

    :return: up to 10 banners that have generated revenue.
    """
    response = client.get_item(
        TableName=CAMPAIGN_BANNERS_TABLE,
        Key={
            'campaign_id': {'N': str(campaign_id)},
            'time': {'N': str(time)}
        }
    )
    # {"banners": {"L": [{"M": {"1": {"N": "20"}, "2": {"N": "2"}, "3": {"N": "64"}, "4": {"N": "5"}}}]}

    banners_list = response.get('Item').get('banners').get('L')[0].get('M')

    # choose random banner
    banner_id = banners_list.get('1').get('N')

    banner_url = f'https://serve-banners.s3.eu-central-1.amazonaws.com/image_{banner_id}.png'

    return banner_url


def show_banner(url: str) -> json:
    response = f'<img src="{url}">'
    return response


def get_time() -> int:
    cur_min = dt.now().minute
    if 0 <= cur_min < 15:
        return 1
    elif 15 <= cur_min < 30:
        return 2
    elif 30 <= cur_min < 45:
        return 3
    else:
        return 4


@app.route('/campaigns/<int:campaign_id>')
def campaign_page(campaign_id: int):
    """
    Get banners belonging to the campaign_id, based on business rules.
    """
    # query banners based on revenue
    time = get_time()
    banner_url = get_top_banners(campaign_id, time)
    return show_banner(banner_url)


if __name__ == '__main__':
    app.run()
