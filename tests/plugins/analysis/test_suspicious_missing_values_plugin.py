import unittest

import pandas as pd
from danda.plugins.analysis.suspicious_missing_values_plugin import SuspiciousMissingValuesPlugin
from danda.plugins.report_collector import ReportCollector
from pandas.testing import assert_frame_equal


class TestSuspiciousMissingValuesPlugin(unittest.TestCase):

    def setUp(self):
        self.report = ReportCollector()
        self.plugin = SuspiciousMissingValuesPlugin(self.report)

    def test_execute_detects_suspicious_missing_values(self):
        df = pd.DataFrame({
            "Age": [25, 999, -999, 40],
            "Status": ["OK", "UNKNOWN", " missing ", "?"],
            "Score": [10, 20, 30, 40],
        })

        result = self.plugin.run(df)

        assert_frame_equal(df, result)

        expected_data = {
            "analysis": {
                "SuspiciousMissingValuesPlugin": {
                    "Age": {
                        999: 1,
                        -999: 1,
                    },
                    "Status": {
                        "UNKNOWN": 1,
                        "MISSING": 1,
                    },
                }
            }
        }

        self.assertEqual(expected_data, self.report.data)

        expected_report = {
            "analysis": {
                "SuspiciousMissingValuesPlugin": (
                    "Suspicious missing value indicators detected:\n"
                    "- Age: 999 (1), -999 (1)\n"
                    "- Status: UNKNOWN (1), MISSING (1)"
                )
            }
        }

        self.assertEqual(expected_report, self.report.report)

    def test_execute_reports_no_suspicious_missing_values(self):
        df = pd.DataFrame({
            "Age": [20, 30, 40],
            "Status": ["OK", "Valid", "Complete"],
        })

        result = self.plugin.run(df)

        assert_frame_equal(df, result)

        expected_data = {
            "analysis": {
                "SuspiciousMissingValuesPlugin": {}
            }
        }

        self.assertEqual(expected_data, self.report.data)

        expected_report = {
            "analysis": {
                "SuspiciousMissingValuesPlugin":
                    "No suspicious missing values detected."
            }
        }

        self.assertEqual(expected_report, self.report.report)

    def test_execute_respects_ignore_case(self):
        df = pd.DataFrame({
            "Status": ["unknown", "Unknown", "UNKNOWN"],
        })

        result = self.plugin.run(df)

        assert_frame_equal(df, result)

        expected_data = {
            "analysis": {
                "SuspiciousMissingValuesPlugin": {
                    "Status": {
                        "UNKNOWN": 3,
                    }
                }
            }
        }

        self.assertEqual(expected_data, self.report.data)

    def test_execute_respects_strip_whitespace(self):
        df = pd.DataFrame({
            "Status": [
                " UNKNOWN ",
                "MISSING ",
                " ? ",
            ],
        })

        result = self.plugin.run(df)

        assert_frame_equal(df, result)

        expected_data = {
            "analysis": {
                "SuspiciousMissingValuesPlugin": {
                    "Status": {
                        "UNKNOWN": 1,
                        "MISSING": 1,
                    }
                }
            }
        }

        self.assertEqual(expected_data, self.report.data)

    def test_execute_detects_numeric_and_string_values(self):
        df = pd.DataFrame({
            "A": [999, 999, 1],
            "B": [-999, 2, -999],
            "C": ["UNKNOWN", "OK", "UNKNOWN"],
        })

        self.plugin.run(df)

        expected_data = {
            "analysis": {
                "SuspiciousMissingValuesPlugin": {
                    "A": {
                        999: 2,
                    },
                    "B": {
                        -999: 2,
                    },
                    "C": {
                        "UNKNOWN": 2,
                    },
                }
            }
        }

        self.assertEqual(expected_data, self.report.data)


if __name__ == '__main__':
    unittest.main()
