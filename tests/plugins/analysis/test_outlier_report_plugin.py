import unittest

import pandas as pd

from danda.plugins.analysis.outlier_report_plugin import OutlierReportPlugin
from danda.plugins.report_collector import ReportCollector


class TestOutlierReportPlugin(unittest.TestCase):

    def setUp(self):
        self.report = ReportCollector()
        self.plugin = OutlierReportPlugin(self.report)

    def test_returns_original_dataframe(self):
        df = pd.DataFrame({
            "a": [1, 2, 3, 100],
        })

        result = self.plugin.run(df)

        pd.testing.assert_frame_equal(result, df)

    def test_detects_zscore_outliers(self):
        config = pd.DataFrame().dg.config
        config.analysis.outlier_method = "zscore"

        df = pd.DataFrame(
            {
                "value": [10] * 20 + [100],
            }
        )

        df.attrs["danda_config"] = config

        report = ReportCollector()
        plugin = OutlierReportPlugin(report)

        plugin.run(df)

        data = report.data["analysis"]["OutlierReport"]

        self.assertEqual(
            data["value"]["method"],
            "ZSCORE",
        )

        self.assertEqual(
            data["value"]["count"],
            1,
        )
    def test_detects_iqr_outliers(self):
        df = pd.DataFrame({
            "age": [10] * 20 + [100],
        })

        self.plugin.run(df)

        data = self.report.data["analysis"]["OutlierReport"]

        self.assertIn("age", data)

        age = data["age"]

        self.assertEqual(age["method"], "IQR")
        self.assertEqual(age["count"], 1)
        self.assertEqual(age["min"], 100)
        self.assertEqual(age["max"], 100)

        self.assertEqual(
            age["examples"],
            [
                {
                    "index": 20,
                    "value": 100,
                }
            ],
        )

    def test_ignores_non_numeric_columns(self):
        df = pd.DataFrame({
            "name": ["Alice", "Bob", "Charlie"],
            "age": [20, 21, 22],
        })

        self.plugin.run(df)

        data = self.report.data["analysis"]["OutlierReport"]

        self.assertNotIn("name", data)

    def test_no_outliers(self):
        df = pd.DataFrame({
            "age": [20, 21, 22, 23, 24],
        })

        self.plugin.run(df)

        data = self.report.data["analysis"]["OutlierReport"]

        self.assertEqual(data, {})

    def test_ignores_constant_columns(self):
        df = pd.DataFrame({
            "age": [10] * 20,
        })

        self.plugin.run(df)

        data = self.report.data["analysis"]["OutlierReport"]

        self.assertEqual(data, {})

    def test_handles_missing_values(self):
        df = pd.DataFrame({
            "age": [10] * 20 + [100, None],
        })

        self.plugin.run(df)

        data = self.report.data["analysis"]["OutlierReport"]

        self.assertEqual(data["age"]["count"], 1)

    def test_report_when_no_outliers(self):
        df = pd.DataFrame({
            "age": [1, 2, 3, 4],
        })

        self.plugin.run(df)

        report = self.report.report["analysis"]["OutlierReport"]

        self.assertEqual(
            report,
            "No outliers detected.",
        )

    def test_report_contains_examples(self):
        df = pd.DataFrame({
            "age": [10] * 20 + [100],
        })

        self.plugin.run(df)

        report = self.report.report["analysis"]["OutlierReport"]

        self.assertIn("Outliers detected:", report)
        self.assertIn("age", report)
        self.assertIn("Method: IQR", report)
        self.assertIn("Outliers: 1", report)
        self.assertIn("Range: 100 to 100", report)
        self.assertIn("Row 20: 100", report)