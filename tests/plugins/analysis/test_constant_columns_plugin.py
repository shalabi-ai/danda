import unittest

import pandas as pd

from danda.plugins.analysis.constant_columns_plugin import ConstantColumnsPlugin
from danda.plugins.report_collector import ReportCollector


class TestConstantColumnsPlugin(unittest.TestCase):

    def setUp(self):
        self.report = ReportCollector()
        self.plugin = ConstantColumnsPlugin(self.report)

    def test_returns_original_dataframe(self):
        df = pd.DataFrame({
            "a": [1, 1],
            "b": [1, 2],
        })

        result = self.plugin.run(df)

        pd.testing.assert_frame_equal(result, df)

    def test_detects_constant_columns(self):
        df = pd.DataFrame({
            "country": ["USA", "USA", "USA"],
            "version": [1, 1, 1],
            "age": [10, 20, 30],
        })

        self.plugin.run(df)

        data = self.report.data["analysis"]["ConstantColumns"]

        self.assertEqual(data, {
            "country": "USA",
            "version": 1,
        })

    def test_ignores_columns_with_multiple_values(self):
        df = pd.DataFrame({
            "a": [1, 2],
            "b": ["x", "y"],
        })

        self.plugin.run(df)

        data = self.report.data["analysis"]["ConstantColumns"]

        self.assertEqual(data, {})

    def test_ignores_all_null_columns(self):
        df = pd.DataFrame({
            "a": [None, None],
            "b": [1, 1],
        })

        self.plugin.run(df)

        data = self.report.data["analysis"]["ConstantColumns"]

        self.assertEqual(data, {
            "b": 1,
        })

    def test_generates_report(self):
        df = pd.DataFrame({
            "country": ["USA", "USA"],
        })

        self.plugin.run(df)

        report = self.report.report["analysis"]["ConstantColumns"]

        self.assertEqual(
            report,
            "Constant columns detected:\n- country: 'USA'",
        )

    def test_generates_empty_report(self):
        df = pd.DataFrame({
            "a": [1, 2],
        })

        self.plugin.run(df)

        report = self.report.report["analysis"]["ConstantColumns"]

        self.assertEqual(
            report,
            "No constant columns detected.",
        )


if __name__ == '__main__':
    unittest.main()
