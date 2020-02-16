"""
Holds the methods that take care of the deduplication step.
"""
from typing import Union, Hashable, Sequence

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
