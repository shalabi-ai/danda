import unittest

import pandas as pd

from danda.plugins.analysis.column_summary_plugin import ColumnSummaryPlugin
from danda.plugins.report_collector import ReportCollector


class TestColumnSummaryPlugin(unittest.TestCase):

    def setUp(self):
        self.report = ReportCollector()
        self.plugin = ColumnSummaryPlugin(self.report)

    def test_returns_original_dataframe(self):
        df = pd.DataFrame({
            "age": [10, 20, None],
            "sex": pd.Series(["M", "F", "F"], dtype="category"),
        })

        result = self.plugin.run(df)

        pd.testing.assert_frame_equal(result, df)

    def test_collects_summary(self):
        df = pd.DataFrame({
            "age": [10.0, None, 20.0],
            "sex": pd.Series(["M", "F", "F"], dtype="category"),
        })

        self.plugin.run(df)

        data = self.report.data["analysis"]["ColumnSummaryPlugin"]

        self.assertEqual(data["age"]["dtype"], "float64")
        self.assertEqual(data["age"]["missing"], 1)
        self.assertEqual(data["age"]["unique"], 2)

        self.assertEqual(data["sex"]["dtype"], "category")
        self.assertEqual(data["sex"]["missing"], 0)
        self.assertEqual(data["sex"]["unique"], 2)

    def test_generates_report(self):
        df = pd.DataFrame({
            "a": [1, None],
        })

        self.plugin.run(df)

        report = self.report.report["analysis"]["ColumnSummaryPlugin"]

        self.assertIn("Column Summary:", report)
        self.assertIn("a", report)
        self.assertIn("Type:", report)
        self.assertIn("Missing: 1", report)
        self.assertIn("Unique: 1", report)


if __name__ == '__main__':
    unittest.main()
