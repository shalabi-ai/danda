import unittest

import pandas as pd
from danda.plugins.clean.sparse_columns_plugin import SparseColumnsPlugin
from danda.plugins.report_collector import ReportCollector
from pandas.testing import assert_frame_equal




class TestSparseColumnsPlugin(unittest.TestCase):

    def setUp(self):
        self.report = ReportCollector()
        self.plugin = SparseColumnsPlugin(self.report)

    def test_execute_removes_sparse_columns(self):
        df = pd.DataFrame({
            "A": [1, 2, 3, 4],
            "B": [None, None, None, None],
            "C": [1, None, None, None],
            "D": [1, 2, 3, 4],
            "E": [None, None, None, 1],
        })

        df.dg.config.cleaning.sparse_columns_enabled = True
        df.dg.config.cleaning.sparse_columns_threshold = 0.75

        result = self.plugin.run(df)

        expected = pd.DataFrame({
            "A": [1, 2, 3, 4],
            "D": [1, 2, 3, 4],
        })

        assert_frame_equal(expected, result)

        expected_data = {
            "clean": {
                "SparseColumnsPlugin": {
                    "columns_removed": 3,
                    "columns": ["B", "C", "E"],
                }
            }
        }

        self.assertEqual(expected_data, self.report.data)

        expected_report = {
            "clean": {
                "SparseColumnsPlugin":
                    "Removed 3 sparse columns: B, C, E"
            }
        }

        self.assertEqual(expected_report, self.report.report)

    def test_execute_removes_no_columns(self):
        df = pd.DataFrame({
            "A": [1, 2],
            "B": [None, 2],
            "C": [3, 4],
        })

        df.dg.config.cleaning.sparse_columns_enabled = True

        result = self.plugin.run(df)

        assert_frame_equal(df, result)

        expected_data = {
            "clean": {
                "SparseColumnsPlugin": {
                    "columns_removed": 0,
                    "columns": [],
                }
            }
        }

        self.assertEqual(expected_data, self.report.data)

        expected_report = {
            "clean": {
                "SparseColumnsPlugin":
                    "No sparse columns removed."
            }
        }

        self.assertEqual(expected_report, self.report.report)

    def test_execute_respects_threshold(self):
        df = pd.DataFrame({
            "A": [1, 2, 3, 4, 5],              # 0%
            "B": [1, None, None, None, None],  # 80%
            "C": [1, 2, None, None, None],     # 60%
        })

        df.dg.config.cleaning.sparse_columns_enabled = True
        df.dg.config.cleaning.sparse_columns_threshold = 0.8

        result = self.plugin.run(df)

        expected = pd.DataFrame({
            "A": [1, 2, 3, 4, 5],
            "C": [1, 2, None, None, None],
        })

        assert_frame_equal(expected, result)

if __name__ == '__main__':
    unittest.main()
