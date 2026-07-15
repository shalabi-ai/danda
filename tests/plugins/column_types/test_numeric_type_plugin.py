import unittest
import pandas as pd
from danda.plugins.column_types.numeric_type_plugin import NumericTypePlugin
from danda.plugins.report_collector import ReportCollector
from pandas.testing import assert_frame_equal
from pandas.api.types import is_numeric_dtype


class TestNumericTypePlugin(unittest.TestCase):

    def setUp(self):
        self.report = ReportCollector()
        self.plugin = NumericTypePlugin(self.report)

    def test_execute_converts_numeric_columns(self):
        df = pd.DataFrame({
            "integers": ["1", "2", "3"],
            "floats": ["1.5", "2.5", "3.5"],
            "text": ["Alice", "Bob", "Charlie"]
        })

        result = self.plugin.run(df, self.report)

        self.assertTrue(is_numeric_dtype(result["integers"]))
        self.assertTrue(is_numeric_dtype(result["floats"]))
        self.assertFalse(is_numeric_dtype(result["text"]))

        expected_data = {'types': {'NumericTypePlugin': ['integers', 'floats']}}
        self.assertEqual(expected_data, self.report.data)

        expected_report = {'types': {'NumericTypePlugin': 'Converted the following columns to numeric: integers, floats'}}
        self.assertEqual(expected_report, self.report.report)


    def test_handles_missing_values(self):
        df = pd.DataFrame({
            "numbers": ["1", None, "3", "4"]
        })

        result = self.plugin.run(df, self.report)

        self.assertTrue(is_numeric_dtype(result["numbers"]))
        self.assertEqual(result["numbers"].isna().sum(), 1)

        expected_data = {'types': {'NumericTypePlugin': ['numbers']}}
        self.assertEqual(expected_data, self.report.data)

        expected_report = {'types': {'NumericTypePlugin': 'Converted the following columns to numeric: numbers'}}
        self.assertEqual(expected_report, self.report.report)

    def test_success_threshold(self):
        df = pd.DataFrame({
            "mixed": ["1", "2", "abc", "4"]
        })

        result = self.plugin._find_numeric_columns(
            df,
            success_threshold=0.75
        )

        self.assertEqual(result, ["mixed"])

        result = self.plugin._find_numeric_columns(
            df,
            success_threshold=1.0
        )

        self.assertEqual(result, [])

    def test_skip_already_numeric_columns(self):
        df = pd.DataFrame({
            "int_col": [1, 2, 3],
            "float_col": [1.5, 2.5, 3.5]
        })

        result = self.plugin._find_numeric_columns(df)

        self.assertEqual(result, [])

        result = self.plugin.run(df)

        assert_frame_equal(df, result)
        expected_data = {'types': {'NumericTypePlugin': []}}
        self.assertEqual(expected_data, self.report.data)

        expected_report = {'types': {'NumericTypePlugin': 'No numeric columns detected.'}}
        self.assertEqual(expected_report, self.report.report)

    def test_skip_boolean_datetime_and_category_columns(self):
        df = pd.DataFrame({
            "boolean": pd.Series(
                [True, False, True],
                dtype="boolean"
            ),
            "datetime": pd.date_range(
                "2024-01-01",
                periods=3
            ),
            "category": pd.Series(
                ["A", "B", "A"],
                dtype="category"
            ),
        })

        result = self.plugin._find_numeric_columns(df)

        self.assertEqual(result, [])

    def test_execute_preserves_non_numeric_columns(self):
        df = pd.DataFrame({
            "name": ["Alice", "Bob", "Charlie"]
        })

        result = self.plugin.run(df, self.report)

        assert_frame_equal(result, df)

        expected_data = {'types': {'NumericTypePlugin': []}}
        self.assertEqual(expected_data, self.report.data)

        expected_report = {'types': {'NumericTypePlugin': 'No numeric columns detected.'}}
        self.assertEqual(expected_report, self.report.report)



if __name__ == "__main__":
    unittest.main()