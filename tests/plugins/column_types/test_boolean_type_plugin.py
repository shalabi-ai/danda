import unittest
import pandas as pd
from pandas.testing import assert_frame_equal

from danda.plugins.column_types.boolean_type_plugin import BooleanTypePlugin
from danda.plugins.report_collector import ReportCollector


class TestBooleanTypePlugin(unittest.TestCase):

    def setUp(self):
        self.report = ReportCollector()
        self.plugin = BooleanTypePlugin(self.report)

    def test_convert_boolean_columns(self):
        df = pd.DataFrame({
            "bool_str": ["True", "False", "TRUE"],
            "bool_int": [1, 0, 1],
            "number": [10, 20, 30]
        })

        result = self.plugin.run(df, self.report)

        expected = pd.DataFrame({
            "bool_str": pd.Series([True, False, True], dtype="boolean"),
            "bool_int": pd.Series([True, False, True], dtype="boolean"),
            "number": [10, 20, 30]
        })

        assert_frame_equal(result, expected)

        expected_data = {'types': {'BooleanTypePlugin': ['bool_str', 'bool_int']}}
        self.assertEqual(expected_data, self.report.data)

        expected_report = {'types': {'BooleanTypePlugin': 'convert these columns to boolean bool_str, bool_int'}}
        self.assertEqual(expected_report, self.report.report)

    def test_preserves_non_boolean_columns(self):
        df = pd.DataFrame({
            "name": ["Alice", "Bob"],
            "age": [20, 25]
        })

        result = self.plugin.run(df, self.report)

        assert_frame_equal(result, df)

        expected_data = {'types': {'BooleanTypePlugin': []}}
        self.assertEqual(expected_data, self.report.data)

        expected_report = {'types': {'BooleanTypePlugin': 'No columns converted'}}
        self.assertEqual(expected_report, self.report.report)

    def test_handles_missing_values(self):
        df = pd.DataFrame({
            "flag": ["True", None, "False"]
        })

        result = self.plugin.run(df, self.report)

        expected = pd.DataFrame({
            "flag": pd.Series([True, pd.NA, False], dtype="boolean")
        })

        assert_frame_equal(result, expected)

        expected_data = {'types': {'BooleanTypePlugin': ['flag']}}
        self.assertEqual(expected_data, self.report.data)

        expected_report = {'types': {'BooleanTypePlugin': 'convert these columns to boolean flag'}}
        self.assertEqual(expected_report, self.report.report)


if __name__ == "__main__":
    unittest.main()


if __name__ == '__main__':
    unittest.main()
