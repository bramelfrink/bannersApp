"""
Holds all the tests for the deduplication lambda
"""
import unittest

import pandas as pd
from pandas._testing import assert_frame_equal

from functions.deduplicate.src.deduplicate import deduplicate_input_clicks


class DeduplicateClickTest(unittest.TestCase):
    def test_no_duplicates_clicks(self):
        input_df = pd.DataFrame(
            {
                'click_id': [1, 2, 3, 4, 5, 6],
                'banner_id': [5, 6, 5, 10, 3, 2],
                'campaign_id': [1, 1, 1, 2, 3, 4]
            }
        )

        results_df = deduplicate_input_clicks(input_df)

        expected_results = input_df

        assert_frame_equal(results_df, expected_results)

    def test_empty_dataframe(self):
        input_df = pd.DataFrame(
            {
                'click_id': [],
                'banner_id': [],
                'campaign_id': []
            }
        )

        results_df = deduplicate_input_clicks(input_df)

        expected_results = input_df

        assert_frame_equal(results_df, expected_results)

    def test_duplicate_clicks(self):
        input_df = pd.DataFrame(
            {
                'click_id': [1, 2, 2, 4, 5, 6],
                'banner_id': [5, 6, 5, 10, 3, 2],
                'campaign_id': [1, 1, 1, 2, 3, 4]
            }
        )

        results_df = deduplicate_input_clicks(input_df)

        expected_results = pd.DataFrame(
            {
                'click_id': [1, 2, 4, 5, 6],
                'banner_id': [5, 6, 10, 3, 2],
                'campaign_id': [1, 1, 2, 3, 4]
            }
        )

        assert_frame_equal(results_df, expected_results)


if __name__ == '__main__':
    unittest.main()
