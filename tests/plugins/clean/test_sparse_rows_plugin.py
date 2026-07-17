import unittest
import pandas as pd
from danda.plugins.clean.sparse_rows_plugin import SparseRowsPlugin
from danda.plugins.report_collector import ReportCollector
from pandas.testing import assert_frame_equal



class TestSparseRowsPlugin(unittest.TestCase):

    def setUp(self):
        self.report = ReportCollector()
        self.plugin = SparseRowsPlugin(self.report)

    def test_execute_removes_sparse_rows(self):
        df = pd.DataFrame({
            "A": [1, 1, None, None, None],
            "B": [2, None, None, None, None],
            "C": [3, None, None, None, None],
            "D": [4, None, None, None, None],
            "E": [5, 5, None, None, None],
        })

        df.dg.config.cleaning.sparse_rows_enabled = True
        df.dg.config.cleaning.sparse_rows_threshold = 0.8

        self.plugin.run(df)

        expected_data = {
            "clean": {
                "SparseRowsPlugin": {
                    "rows_removed": 3,
                    "indices": [2, 3, 4],
                }
            }
        }

        self.assertEqual(expected_data, self.report.data)

        expected_report = {
            "clean": {
                "SparseRowsPlugin": "Removed 3 sparse rows."
            }
        }

        self.assertEqual(expected_report, self.report.report)

    def test_execute_removes_no_rows(self):
        df = pd.DataFrame({
            "A": [1, None],
            "B": [2, 2],
            "C": [3, 3],
            "D": [4, 4],
            "E": [5, 5],
        })

        df.dg.config.cleaning.sparse_rows_enabled = True

        result = self.plugin.run(df)

        assert_frame_equal(df, result)

        expected_data = {
            "clean": {
                "SparseRowsPlugin": {
                    "rows_removed": 0,
                    "indices": [],
                }
            }
        }

        self.assertEqual(expected_data, self.report.data)

        expected_report = {
            "clean": {
                "SparseRowsPlugin": "No sparse rows removed."
            }
        }

        self.assertEqual(expected_report, self.report.report)

    def test_execute_respects_threshold(self):
        df = pd.DataFrame({
            "A": [1, None],
            "B": [None, None],
            "C": [None, None],
            "D": [None, 4],
            "E": [5, 5],
        })

        df.dg.config.cleaning.sparse_rows_enabled = True
        df.dg.config.cleaning.sparse_rows_threshold = 0.6

        result = self.plugin.run(df)

        expected = pd.DataFrame(columns=["A", "B", "C", "D", "E"])

        self.assertEqual(expected.size, result.size)
