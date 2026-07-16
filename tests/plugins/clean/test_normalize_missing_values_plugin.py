import unittest
import pandas as pd
import danda # noqa: F401  # registers the pandas accessor
from danda.plugins.clean.normalize_missing_values_plugin import NormalizeMissingValuesPlugin
from danda.plugins.report_collector import ReportCollector


class TestNormalizeMissingValuesPlugin(unittest.TestCase):

    def setUp(self):
        self.report = ReportCollector()
        self.plugin = NormalizeMissingValuesPlugin(self.report)

    def test_execute_normalizes_missing_values(self):
        df = pd.DataFrame({
            "name": ["Alice", "NULL", "Bob", "", "None"],
            "age": ["10", "20", "30", "40", "50"],
        })

        result = self.plugin.run(df)

        self.assertEqual(result["name"].isna().sum(), 3)
        self.assertEqual(result["age"].isna().sum(), 0)

        expected_data = {
            "clean": {
                "NormalizeMissingValuesPlugin": {
                    "name": 3,
                }
            }
        }
        self.assertEqual(expected_data, self.report.data)

        expected_report = {
            "clean": {
                "NormalizeMissingValuesPlugin":
                    "Normalized 3 missing value(s) across 1 column(s)."
            }
        }
        self.assertEqual(expected_report, self.report.report)

    def test_execute_does_not_modify_non_matching_values(self):
        df = pd.DataFrame({
            "name": ["Alice", "Unknown", "N/A", "-", "?"],
        })

        result = self.plugin.run(df)

        self.assertEqual(result["name"].isna().sum(), 0)

        expected_data = {
            "clean": {
                "NormalizeMissingValuesPlugin": {}
            }
        }
        self.assertEqual(expected_data, self.report.data)

        expected_report = {
            "clean": {
                "NormalizeMissingValuesPlugin":
                    "No missing values were normalized."
            }
        }
        self.assertEqual(expected_report, self.report.report)

    def test_execute_is_case_insensitive(self):
        df = pd.DataFrame({
            "value": [
                "NULL",
                "Null",
                "null",
                "NONE",
                "NaN",
                "<NA>",
            ]
        })

        result = self.plugin.run(df)

        self.assertEqual(result["value"].isna().sum(), 6)

    def test_execute_strips_whitespace(self):
        df = pd.DataFrame({
            "value": [
                " null ",
                "  None",
                "NaN  ",
                "   ",
            ]
        })

        result = self.plugin.run(df)

        self.assertEqual(result["value"].isna().sum(), 4)

    def test_execute_ignores_non_string_values(self):
        df = pd.DataFrame({
            "mixed": [1, 2.5, True, pd.NA],
        })

        result = self.plugin.run(df)

        self.assertEqual(result["mixed"].isna().sum(), 1)

        pd.testing.assert_series_equal(
            result["mixed"],
            df["mixed"],
            check_names=False,
        )

    def test_execute_respects_custom_null_values(self):
        df = pd.DataFrame({
            "status": ["missing", "ok", "missing"],
        })

        df.dg.config.missing.normalize_values = (
            "",
            "missing",
        )

        result = self.plugin.run(df)

        self.assertEqual(result["status"].isna().sum(), 2)

    def test_execute_no_white_space(self):
        df = pd.DataFrame({
                "status": ["  ", " null ", "null"],
            })

        df.dg.config.missing.normalize_strip_whitespace = False

        result = self.plugin.run(df)

        self.assertEqual(result["status"].isna().sum(), 1)

    def test_execute_no_upper(self):
        df = pd.DataFrame({
                "status": ["  ", "NULL", "null"],
            })

        df.dg.config.missing.normalize_ignore_case = False

        result = self.plugin.run(df)

        self.assertEqual(result["status"].isna().sum(), 2)

if __name__ == '__main__':
    unittest.main()
