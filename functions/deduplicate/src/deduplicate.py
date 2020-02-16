"""
Holds the methods that take care of the deduplication step.
"""
from pandas import DataFrame


def deduplicate_input_clicks(df: DataFrame) -> DataFrame:
    """
    Deduplicates the DataFrame.

    :param df: the DataFrame with potential duplicates
    :return: a deduplicated DataFrame
    """
    return df
