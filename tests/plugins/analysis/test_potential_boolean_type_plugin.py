import unittest
import pandas as pd
from danda.plugins.analysis.potential_boolean_type_plugin import PotentialBooleanTypePlugin
from danda.plugins.report_collector import ReportCollector
from pandas.testing import assert_frame_equal

class TestPotentialBooleanTypePlugin(unittest.TestCase):

    def setUp(self):
        self.report = ReportCollector()
        self.plugin = PotentialBooleanTypePlugin(self.report)

    def test_execute_returns_original_dataframe(self):
        df = pd.DataFrame({
            "A": ["Y", "N"],
            "B": [1, 2]
        })

        result = self.plugin.run(df)

        assert_frame_equal(result, df)

        expected_data = {'analysis': {'PotentialBooleanTypePlugin': {'A': ['y', 'n'], 'B': [1, 2]}}}
        self.assertEqual(expected_data, self.report.data)

        expected_report = {'analysis': {'PotentialBooleanTypePlugin': "Columns that may represent boolean values:\n - A: ['y', 'n']\n - B: [np.int64(1), np.int64(2)]"}}
        self.assertEqual(expected_report, self.report.report)

    def test_find_potential_boolean_columns(self):
        df = pd.DataFrame({
            "gender": ["M", "F", "M"],
            "active": ["Y", "N", "Y"],
            "status": ["Open", "Closed", "Open"],
            "flag": [1, 0, 1],               # already boolean-like
            "bool": [True, False, True],     # already boolean-like
            "color": ["Red", "Blue", "Green"],  # 3 unique values
            "number": [1, 2, 3]
        })

        result = self.plugin.run(df)

        assert_frame_equal(result, df)

        expected_data = {'analysis': {'PotentialBooleanTypePlugin': {'active': ['y', 'n'], 'gender': ['m', 'f'], 'status': ['open', 'closed']}}}
        self.assertEqual(expected_data, self.report.data)

        expected_report = {'analysis': {'PotentialBooleanTypePlugin': "Columns that may represent boolean values:\n - gender: ['m', 'f']\n - active: ['y', 'n']\n - status: ['open', 'closed']"}}
        self.assertEqual(expected_report, self.report.report)

    def test_ignore_case_space(self):
        df = pd.DataFrame({
            "color": ["Red", "Blue", "BLUE", "red", "  red", "red   ", "   ReD   "]
        })

        self.plugin.run(df)

        expected_data = {'analysis': {'PotentialBooleanTypePlugin': {'color': ['red', 'blue']}}}
        self.assertEqual(expected_data, self.report.data)

        expected_report = {'analysis': {'PotentialBooleanTypePlugin': "Columns that may represent boolean values:\n - color: ['red', 'blue']"}}
        self.assertEqual(expected_report, self.report.report)

    def test_ignore_columns_with_more_than_two_unique_values(self):
        df = pd.DataFrame({
            "color": ["Red", "Blue", "Green", "Red"]
        })

        self.plugin.run(df)

        expected_data = {'analysis': {'PotentialBooleanTypePlugin': {}}}
        self.assertEqual(expected_data, self.report.data)

        expected_report = {'analysis': {'PotentialBooleanTypePlugin': 'No potential boolean columns found.'}}
        self.assertEqual(expected_report, self.report.report)

    def test_ignore_existing_boolean_columns(self):
        df = pd.DataFrame({
            "bool1": [True, False, True],
            "bool2": [1, 0, 1],
            "bool3": ["True", "False", "True"]
        })

        self.plugin.run(df)

        expected_data = {'analysis': {'PotentialBooleanTypePlugin': {}}}
        self.assertEqual(expected_data, self.report.data)

        expected_report = {'analysis': {'PotentialBooleanTypePlugin': 'No potential boolean columns found.'}}
        self.assertEqual(expected_report, self.report.report)

    def test_ignore_single_unique_value(self):
        df = pd.DataFrame({
            "constant": ["Y", "Y", "Y"]
        })

        self.plugin.run(df)

        expected_data = {'analysis': {'PotentialBooleanTypePlugin': {}}}
        self.assertEqual(expected_data, self.report.data)

        expected_report = {'analysis': {'PotentialBooleanTypePlugin': 'No potential boolean columns found.'}}
        self.assertEqual(expected_report, self.report.report)

    def test_handles_missing_values(self):
        df = pd.DataFrame({
            "approved": ["Yes", None, "No", None]
        })

        self.plugin.run(df)

        expected_data = {'analysis': {'PotentialBooleanTypePlugin': {'approved': ['yes', 'no']}}}
        self.assertEqual(expected_data, self.report.data)

        expected_report = {'analysis': {'PotentialBooleanTypePlugin': "Columns that may represent boolean values:\n - approved: ['yes', 'no']"}}
        self.assertEqual(expected_report, self.report.report)


if __name__ == '__main__':
    unittest.main()
