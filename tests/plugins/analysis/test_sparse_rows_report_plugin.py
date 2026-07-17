import unittest

import pandas as pd
from pandas.testing import assert_frame_equal

from danda.plugins.analysis.sparse_rows_report_plugin import (
    SparseRowsReportPlugin,
)
from danda.plugins.report_collector import ReportCollector


class TestSparseRowsReportPlugin(unittest.TestCase):

    def setUp(self):
        self.report = ReportCollector()
        self.plugin = SparseRowsReportPlugin(self.report)

    def test_execute_does_not_modify_dataframe(self):
        df = pd.DataFrame({
            "A": [1, None],
            "B": [None, 2],
        })

        result = self.plugin.run(df)

        assert_frame_equal(df, result)

    def test_report_sparse_rows(self):
        df = pd.DataFrame({
            "A": [1, None, None],
            "B": [None, None, 3],
            "C": [None, None, None],
            "D": [4, None, None],
        })

        df.dg.config.analysis.sparse_rows_report_threshold = 0.5

        self.plugin.run(df)

        expected_data = {
            "analysis": {
                "SparseRowsReportPlugin": [
                    {
                        "index": 1,
                        "missing": 4,
                        "total": 4,
                        "percent": 100.0,
                    },
                    {
                        "index": 2,
                        "missing": 3,
                        "total": 4,
                        "percent": 75.0,
                    },
                    {
                        "index": 0,
                        "missing": 2,
                        "total": 4,
                        "percent": 50.0,
                    },
                ]
            }
        }

        self.assertEqual(expected_data, self.report.data)

        expected_report = {
            "analysis": {
                "SparseRowsReportPlugin": (
                    "Rows with many missing values:\n"
                    "- Row 1: 4/4 missing (100.0%)\n"
                    "- Row 2: 3/4 missing (75.0%)\n"
                    "- Row 0: 2/4 missing (50.0%)"
                )
            }
        }

        self.assertEqual(expected_report, self.report.report)

    def test_report_respects_threshold(self):
        df = pd.DataFrame({
            "A": [1, None],
            "B": [2, None],
            "C": [3, None],
            "D": [None, None],
        })

        df.dg.config.analysis.sparse_rows_report_threshold = 0.75

        self.plugin.run(df)

        expected_data = {
            "analysis": {
                "SparseRowsReportPlugin": [
                    {
                        "index": 1,
                        "missing": 4,
                        "total": 4,
                        "percent": 100.0,
                    }
                ]
            }
        }

        self.assertEqual(expected_data, self.report.data)

    def test_report_respects_max_rows(self):
        df = pd.DataFrame({
            "A": [None, None, None],
            "B": [None, None, 1],
            "C": [None, 1, 1],
            "D": [1, 1, 1],
        })

        df.dg.config.analysis.sparse_rows_report_threshold = 0.25
        df.dg.config.analysis.sparse_rows_report_max_rows = 2

        self.plugin.run(df)

        expected_data = {
            "analysis": {
                "SparseRowsReportPlugin": [
                    {
                        "index": 0,
                        "missing": 3,
                        "total": 4,
                        "percent": 75.0,
                    },
                    {
                        "index": 1,
                        "missing": 2,
                        "total": 4,
                        "percent": 50.0,
                    },
                ]
            }
        }

        self.assertEqual(expected_data, self.report.data)

    def test_report_no_sparse_rows(self):
        df = pd.DataFrame({
            "A": [1, 2],
            "B": [3, None],
            "C": [4, 5],
        })

        df.dg.config.analysis.sparse_rows_report_threshold = 0.5

        self.plugin.run(df)

        expected_data = {
            "analysis": {
                "SparseRowsReportPlugin": []
            }
        }

        self.assertEqual(expected_data, self.report.data)

        expected_report = {
            "analysis": {
                "SparseRowsReportPlugin": "No sparse rows detected."
            }
        }

        self.assertEqual(expected_report, self.report.report)

    def test_empty_dataframe(self):
        df = pd.DataFrame()

        self.plugin.run(df)

        expected_data = {
            "analysis": {
                "SparseRowsReportPlugin": []
            }
        }

        self.assertEqual(expected_data, self.report.data)


if __name__ == '__main__':
    unittest.main()
