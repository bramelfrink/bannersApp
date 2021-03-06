"""
Holds the methods that take care of the deduplication step.
"""
import os
from typing import Union, Hashable, Sequence

import boto3
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


def find_duplicates(df: DataFrame, deduplicated_df: DataFrame) -> DataFrame:
    """
    Finds all duplicates by checking which click_ids were in df, but are no longer in deduplicated_df.

    :param df: the original df
    :param deduplicated_df: the deduplicated df
    :return: a dataframe with all the duplicates
    """
    duplicate_df = df[(~df.click_id.isin(deduplicated_df.click_id))]
    return duplicate_df


class DynamoDBDeduplication:
    """
    Class that contains methods for the deduplication step
    """

    def __init__(self, column: str, table: str):
        self.column = column
        self.table = table
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
            TableName=self.table,
            Key={
                self.column: {
                    'N': str(id)
                }
            }
        )
        unique = 'Item' not in item
        if unique:
            # Item is not yet stored in DynamoDB, so register it now.
            self.store_item(id)
        return 'Item' not in item

    def store_item(self, id: int):
        """
        Stores the item in DynamoDB.
        Only store the identifier. The table in which these identifiers are stored should only be used to
        check for duplicates.
        """
        self.client.put_item(
            TableName=self.table,
            Item={
                self.column: {
                    'N': str(id)
                }
            }
        )
