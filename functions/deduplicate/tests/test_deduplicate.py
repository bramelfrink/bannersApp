"""
Holds all the tests for the deduplication lambda
"""
import unittest

import pandas as pd
from pandas import DataFrame
from pandas._testing import assert_frame_equal

from functions.deduplicate.src.deduplicate import deduplicate_input


def compare_dataframes(result: DataFrame, expected: DataFrame):
    """
    Resets the index of the result, because the index might have gaps after deduplication and checks if the
    result and expected are equal.
    """
    assert_frame_equal(result.reset_index(drop=True), expected)


class DeduplicateClickTest(unittest.TestCase):
    def test_no_duplicates_clicks(self):
        input_df = pd.DataFrame(
            {
                'click_id': [1, 2, 3, 4, 5, 6],
                'banner_id': [5, 6, 5, 10, 3, 2],
                'campaign_id': [1, 1, 1, 2, 3, 4]
            }
        )

        results_df = deduplicate_input(input_df, 'click_id')

        expected_results = input_df

        compare_dataframes(results_df, expected_results)

    def test_empty_dataframe(self):
        input_df = pd.DataFrame(
            {
                'click_id': [],
                'banner_id': [],
                'campaign_id': []
            }
        )

        results_df = deduplicate_input(input_df, 'click_id')

        expected_results = input_df

        compare_dataframes(results_df, expected_results)

    def test_duplicate_clicks(self):
        input_df = pd.DataFrame(
            {
                'click_id': [1, 2, 2, 4, 5, 6],
                'banner_id': [5, 6, 5, 10, 3, 2],
                'campaign_id': [1, 1, 1, 2, 3, 4]
            }
        )

        results_df = deduplicate_input(input_df, 'click_id')

        expected_results = pd.DataFrame(
            {
                'click_id': [1, 2, 4, 5, 6],
                'banner_id': [5, 6, 10, 3, 2],
                'campaign_id': [1, 1, 2, 3, 4]
            }
        )

        compare_dataframes(results_df, expected_results)


if __name__ == '__main__':
    unittest.main()
