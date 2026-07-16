import unittest

import pandas as pd
from danda.plugins.analysis.missing_values_report_plugin import MissingValuesReportPlugin
from danda.plugins.report_collector import ReportCollector
from pandas.testing import assert_frame_equal


class TestMissingValuesReportPlugin(unittest.TestCase):

    def setUp(self):
        self.report = ReportCollector()
        self.plugin = MissingValuesReportPlugin(self.report)

    def test_execute_reports_missing_values(self):
        df = pd.DataFrame({
            "Age": [20, None, 30, None],
            "Salary": [1000, None, None, None],
            "Email": ["a@test.com", "b@test.com", None, "d@test.com"],
            "Name": ["Alice", "Bob", "Charlie", "David"],
        })

        result = self.plugin.run(df)

        assert_frame_equal(df, result)

        expected_data = {
            "analysis": {
                "MissingValuesReportPlugin": {
                    "Age": {
                        "count": 2,
                        "percent": 50.0,
                    },
                    "Salary": {
                        "count": 3,
                        "percent": 75.0,
                    },
                    "Email": {
                        "count": 1,
                        "percent": 25.0,
                    },
                }
            }
        }

        self.assertEqual(expected_data, self.report.data)

        expected_report = {
            "analysis": {
                "MissingValuesReportPlugin": (
                    "Missing values detected:\n"
                    "- Salary: 3 (75.0%)\n"
                    "- Age: 2 (50.0%)\n"                   
                    "- Email: 1 (25.0%)"
                )
            }
        }

        self.assertEqual(expected_report, self.report.report)

    def test_execute_reports_no_missing_values(self):
        df = pd.DataFrame({
            "Age": [20, 25, 30],
            "Salary": [1000, 2000, 3000],
        })

        result = self.plugin.run(df)

        assert_frame_equal(df, result)

        expected_data = {
            "analysis": {
                "MissingValuesReportPlugin": {}
            }
        }

        self.assertEqual(expected_data, self.report.data)

        expected_report = {
            "analysis": {
                "MissingValuesReportPlugin":
                    "No missing values detected."
            }
        }

        self.assertEqual(expected_report, self.report.report)

    def test_execute_ignores_columns_without_missing_values(self):
        df = pd.DataFrame({
            "A": [1, None, 3],
            "B": [1, 2, 3],
        })

        self.plugin.run(df)

        expected_data = {
            "analysis": {
                "MissingValuesReportPlugin": {
                    "A": {
                        "count": 1,
                        "percent": 33.3,
                    }
                }
            }
        }

        self.assertEqual(expected_data, self.report.data)

    def test_report_sorts_by_missing_percentage_descending(self):
        df = pd.DataFrame({
            "Age": [20, None, 30, None],                  # 50%
            "Salary": [None, None, None, 1000],           # 75%
            "Email": ["a@test.com", None, "c@test.com", "d@test.com"],  # 25%
        })

        self.plugin.run(df)

        expected_report = {
            "analysis": {
                "MissingValuesReportPlugin": (
                    "Missing values detected:\n"
                    "- Salary: 3 (75.0%)\n"
                    "- Age: 2 (50.0%)\n"
                    "- Email: 1 (25.0%)"
                )
            }
        }

        self.assertEqual(expected_report, self.report.report)

    def test_report_sorts_by_count_when_percentages_are_equal(self):
        df = pd.DataFrame({
            "A": [1, None, None, 4],                  # 2/4 = 50%
            "B": [1, 2, None, None],                  # 2/4 = 50%
            "C": [1, None, 3, 4],                     # 1/4 = 25%
        })

        self.plugin.run(df)

        expected_report = {
            "analysis": {
                "MissingValuesReportPlugin": (
                    "Missing values detected:\n"
                    "- A: 2 (50.0%)\n"
                    "- B: 2 (50.0%)\n"
                    "- C: 1 (25.0%)"
                )
            }
        }

        self.assertEqual(expected_report, self.report.report)

if __name__ == '__main__':
    unittest.main()
