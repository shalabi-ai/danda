import unittest
import pandas as pd
from danda.plugins.column_types.potential_boolean_type_plugin import PotentialBooleanTypePlugin
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

        expected_data = {'types': {'PotentialBooleanTypePlugin': {'A': ['Y', 'N'], 'B': [1, 2]}}}
        self.assertEqual(expected_data, self.report.data)

        expected_report = {'types': {'PotentialBooleanTypePlugin': "Potential boolean columns detected:\n - A: ['Y', 'N']\n - B: [np.int64(1), np.int64(2)]"}}
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

        expected_data = {'types': {'PotentialBooleanTypePlugin': {'active': ['Y', 'N'], 'gender': ['M', 'F'], 'status': ['Open', 'Closed']}}}
        self.assertEqual(expected_data, self.report.data)

        expected_report = {'types': {'PotentialBooleanTypePlugin': "Potential boolean columns detected:\n - gender: ['M', 'F']\n - active: ['Y', 'N']\n - status: ['Open', 'Closed']"}}
        self.assertEqual(expected_report, self.report.report)

    def test_ignore_columns_with_more_than_two_unique_values(self):
        df = pd.DataFrame({
            "color": ["Red", "Blue", "Green", "Red"]
        })

        self.plugin.run(df)

        expected_data = {'types': {'PotentialBooleanTypePlugin': {}}}
        self.assertEqual(expected_data, self.report.data)

        expected_report = {'types': {'PotentialBooleanTypePlugin': 'No potential boolean columns found.'}}
        self.assertEqual(expected_report, self.report.report)

    def test_ignore_existing_boolean_columns(self):
        df = pd.DataFrame({
            "bool1": [True, False, True],
            "bool2": [1, 0, 1],
            "bool3": ["True", "False", "True"]
        })

        self.plugin.run(df)

        expected_data = {'types': {'PotentialBooleanTypePlugin': {}}}
        self.assertEqual(expected_data, self.report.data)

        expected_report = {'types': {'PotentialBooleanTypePlugin': 'No potential boolean columns found.'}}
        self.assertEqual(expected_report, self.report.report)

    def test_ignore_single_unique_value(self):
        df = pd.DataFrame({
            "constant": ["Y", "Y", "Y"]
        })

        self.plugin.run(df)

        expected_data = {'types': {'PotentialBooleanTypePlugin': {}}}
        self.assertEqual(expected_data, self.report.data)

        expected_report = {'types': {'PotentialBooleanTypePlugin': 'No potential boolean columns found.'}}
        self.assertEqual(expected_report, self.report.report)

    def test_handles_missing_values(self):
        df = pd.DataFrame({
            "approved": ["Yes", None, "No", None]
        })

        self.plugin.run(df)

        expected_data = {'types': {'PotentialBooleanTypePlugin': {'approved': ['Yes', 'No']}}}
        self.assertEqual(expected_data, self.report.data)

        expected_report = {'types': {'PotentialBooleanTypePlugin': "Potential boolean columns detected:\n - approved: ['Yes', 'No']"}}
        self.assertEqual(expected_report, self.report.report)


if __name__ == '__main__':
    unittest.main()
