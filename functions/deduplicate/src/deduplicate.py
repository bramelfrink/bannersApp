"""
Holds the methods that take care of the deduplication step.
"""
import os
from typing import Union, Hashable, Sequence

import boto as boto
import boto3
import pandas as pd
from pandas import DataFrame


def deduplicate_input(df: DataFrame, subset: Union[Hashable, Sequence[Hashable]]) -> DataFrame:
    """
    Deduplicates the DataFrame.

    :param df: the DataFrame with potential duplicates
    :param subset: the columns to consider when deduplicating
    :return: a deduplicated DataFrame
    """
    deduplicated_df = df.drop_duplicates(subset)
    return deduplicated_df


class DynamoDBDeduplication:

    def __init__(self, column: str):
        self.column = column
        self.client = boto3.client('dynamodb')

    def is_unique(self, id: int) -> bool:
        """
        Queries DynamoDB to check if the id has already been seen before.

        :param id: the id to check
        :param column: the column name of the id
        :param dbclient: the DynamoDB client
        :return: True if it is a duplicate, false otherwise
        """
        item = self.client.get_item(
            TableName=os.environ['tableName'],
            Key={
                self.column: {
                    'N': str(id)
                }
            }
        )
        return 'Item' not in item


if __name__ == '__main__':
    os.environ['tableName'] = 'Banners-DynamoDBClicks-16653UQLD7IX7'
    df = pd.DataFrame(
        {
            'click_id': [1,2,3,123]
        }
    )

    db = DynamoDBDeduplication('click_id')
    deduplicated_df = df[df['click_id'].apply(db.is_unique)]
    print(deduplicated_df.head())