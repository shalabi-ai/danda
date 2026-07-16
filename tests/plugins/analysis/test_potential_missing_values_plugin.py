import unittest
import pandas as pd
from danda.plugins.analysis.potential_missing_values_plugin import PotentialMissingValuesPlugin
from danda.plugins.report_collector import ReportCollector
from pandas.testing import assert_frame_equal

class TestPotentialMissingValuesPlugin(unittest.TestCase):

    def setUp(self):
        self.report = ReportCollector()
        self.plugin = PotentialMissingValuesPlugin(self.report)

    def test_execute_reports_potential_missing_values(self):
        df = pd.DataFrame({
            "status": [
                "OK",
                "N/A",
                "Unknown",
                "N/A",
                "-",
            ],
            "city": [
                "Berlin",
                "Paris",
                "London",
                "Rome",
                "Madrid",
            ],
        })

        result = self.plugin.run(df)

        assert_frame_equal(df, result)

        expected_data = {
            "analysis": {
                "PotentialMissingValuesPlugin": {
                    "status": {
                        "N/A": 2,
                        "Unknown": 1,
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
                    "- status: N/A (2), Unknown (1), - (1)"
                )
            }
        }
        self.assertEqual(expected_report, self.report.report)

    def test_execute_reports_no_potential_missing_values(self):
        df = pd.DataFrame({
            "status": ["OK", "YES", "NO"],
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

    def test_execute_is_case_insensitive(self):
        df = pd.DataFrame({
            "status": [
                "unknown",
                "Unknown",
                "UNKNOWN",
            ]
        })

        self.plugin.run(df)

        expected_data = {
            "analysis": {
                "PotentialMissingValuesPlugin": {
                    "status": {
                        "unknown": 1,
                        "Unknown": 1,
                        "UNKNOWN": 1,
                    }
                }
            }
        }

        self.assertEqual(expected_data, self.report.data)

    def test_execute_strips_whitespace(self):
        df = pd.DataFrame({
            "status": [
                " N/A ",
                " Unknown",
                "- ",
            ]
        })

        self.plugin.run(df)

        expected_data = {
            "analysis": {
                "PotentialMissingValuesPlugin": {
                    "status": {
                        " N/A ": 1,
                        " Unknown": 1,
                        "- ": 1,
                    }
                }
            }
        }

        self.assertEqual(expected_data, self.report.data)

    def test_execute_respects_custom_values(self):
        df = pd.DataFrame({
            "status": [
                "TBC",
                "Done",
                "TBC",
            ]
        })

        df.dg.config.analysis.empty_value_values = ("tbc",)

        self.plugin.run(df)

        expected_data = {
            "analysis": {
                "PotentialMissingValuesPlugin": {
                    "status": {
                        "TBC": 2,
                    }
                }
            }
        }

        self.assertEqual(expected_data, self.report.data)


if __name__ == '__main__':
    unittest.main()
