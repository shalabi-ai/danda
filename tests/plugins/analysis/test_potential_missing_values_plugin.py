import unittest
import pandas as pd
from danda.plugins.analysis.potential_missing_values_plugin import PotentialMissingValuesPlugin
from danda.plugins.report_collector import ReportCollector
from pandas.testing import assert_frame_equal

class TestPotentialMissingValuesPlugin(unittest.TestCase):

    def setUp(self):
        self.report = ReportCollector()
        self.plugin = PotentialMissingValuesPlugin(self.report)

    def test_execute_detects_potential_missing_values(self):
        df = pd.DataFrame({
            "status": [
                "N/A",
                "unknown",
                "-",
                "OK",
                None,
            ]
        })

        result = self.plugin.run(df)

        assert_frame_equal(df, result)

        expected_data = {
            "analysis": {
                "PotentialMissingValuesPlugin": {
                    "status": {
                        "n/a": 1,
                        "-": 1,
                    }
                }
            }
        }

        self.assertEqual(expected_data, self.report.data)

        expected_report = {
            "analysis": {
                "PotentialMissingValuesPlugin": (
                    "Potential missing values detected:\n"
                    "- status: n/a (1), - (1)"
                )
            }
        }

        self.assertEqual(expected_report, self.report.report)

    def test_execute_merges_case_variants(self):
        df = pd.DataFrame({
            "status": [
                "n/a",
                "N/a",
                "N/A",
                " n/A ",
            ]
        })

        result = self.plugin.run(df)

        assert_frame_equal(df, result)

        expected_data = {
            "analysis": {
                "PotentialMissingValuesPlugin": {
                    "status": {
                        "n/a": 4,
                    }
                }
            }
        }

        self.assertEqual(expected_data, self.report.data)

        expected_report = {
            "analysis": {
                "PotentialMissingValuesPlugin": (
                    "Potential missing values detected:\n"
                    "- status: n/a (4)"
                )
            }
        }

        self.assertEqual(expected_report, self.report.report)

    def test_execute_respects_ignore_case_disabled(self):
        df = pd.DataFrame({
            "status": [
                "n/a",
                "N/A",
            ]
        })

        df.dg.config.analysis.empty_value_ignore_case = False

        self.plugin.run(df)

        expected_data = {
            "analysis": {
                "PotentialMissingValuesPlugin": {
                    "status": {
                        "n/a": 1,
                    }
                }
            }
        }

        self.assertEqual(expected_data, self.report.data)

    def test_execute_respects_strip_whitespace_disabled(self):
        df = pd.DataFrame({
            "status": [
                " N/A ",
                "N/A",
            ]
        })

        df.dg.config.analysis.empty_value_strip_whitespace = False

        self.plugin.run(df)

        expected_data = {
            "analysis": {
                "PotentialMissingValuesPlugin": {
                    "status": {
                        "n/a": 1,
                    }
                }
            }
        }

        self.assertEqual(expected_data, self.report.data)

    def test_execute_reports_no_potential_missing_values(self):
        df = pd.DataFrame({
            "status": [
                "Active",
                "Inactive",
                "Complete",
            ]
        })

        result = self.plugin.run(df)

        assert_frame_equal(df, result)

        expected_data = {
            "analysis": {
                "PotentialMissingValuesPlugin": {}
            }
        }

        self.assertEqual(expected_data, self.report.data)

        expected_report = {
            "analysis": {
                "PotentialMissingValuesPlugin":
                    "No potential missing values detected."
            }
        }

        self.assertEqual(expected_report, self.report.report)


if __name__ == '__main__':
    unittest.main()
