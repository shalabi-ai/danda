import unittest

import pandas as pd
from pandas.testing import assert_frame_equal

from danda.plugins.analysis.missing_values_summary_plugin import (
    MissingValuesSummaryPlugin,
)
from danda.plugins.report_collector import ReportCollector


class TestMissingValuesSummaryPlugin(unittest.TestCase):

    def setUp(self):
        self.report = ReportCollector()
        self.plugin = MissingValuesSummaryPlugin(self.report)

    def test_execute_does_not_modify_dataframe(self):
        df = pd.DataFrame({
            "A": [1, None, 3],
            "B": [None, 2, 3],
        })

        result = self.plugin.run(df)

        assert_frame_equal(df, result)

    def test_report_summary(self):
        df = pd.DataFrame({
            "A": [1, None, 3],
            "B": [None, 2, 3],
            "C": [1, 2, 3],
        })

        self.plugin.run(df)

        expected_data = {
            "analysis": {
                "MissingValuesSummaryPlugin": {
                    "rows": 3,
                    "columns": 3,
                    "missing_cells": 2,
                    "missing_percent": 22.2,
                    "columns_with_missing": 2,
                    "rows_with_missing": 2,
                    "complete_rows": 1,
                    "complete_rows_percent": 33.3,
                }
            }
        }

        self.assertEqual(expected_data, self.report.data)

        expected_report = {
            "analysis": {
                "MissingValuesSummaryPlugin": (
                    "Missing Value Summary\n"
                    "Rows: 3\n"
                    "Columns: 3\n\n"
                    "Missing cells: 2 (22.2%)\n"
                    "Columns with missing: 2\n"
                    "Rows with missing: 2\n"
                    "Complete rows: 1 (33.3%)"
                )
            }
        }

        self.assertEqual(expected_report, self.report.report)

    def test_report_no_missing_values(self):
        df = pd.DataFrame({
            "A": [1, 2, 3],
            "B": [4, 5, 6],
        })

        self.plugin.run(df)

        expected_data = {
            "analysis": {
                "MissingValuesSummaryPlugin": {
                    "rows": 3,
                    "columns": 2,
                    "missing_cells": 0,
                    "missing_percent": 0.0,
                    "columns_with_missing": 0,
                    "rows_with_missing": 0,
                    "complete_rows": 3,
                    "complete_rows_percent": 100.0,
                }
            }
        }

        self.assertEqual(expected_data, self.report.data)

    def test_empty_dataframe(self):
        df = pd.DataFrame()

        self.plugin.run(df)

        expected_data = {
            "analysis": {
                "MissingValuesSummaryPlugin": {
                    "rows": 0,
                    "columns": 0,
                    "missing_cells": 0,
                    "missing_percent": 0.0,
                    "columns_with_missing": 0,
                    "rows_with_missing": 0,
                    "complete_rows": 0,
                    "complete_rows_percent": 0.0,
                }
            }
        }

        self.assertEqual(expected_data, self.report.data)


if __name__ == '__main__':
    unittest.main()
