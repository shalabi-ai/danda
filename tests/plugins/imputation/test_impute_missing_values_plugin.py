import unittest

import pandas as pd
from danda.plugins.imputation.impute_missing_values_plugin import ImputeMissingValuesPlugin
from danda.plugins.report_collector import ReportCollector
from pandas.api.types import is_categorical_dtype
from pandas.testing import assert_frame_equal


class TestImputeMissingValuesPlugin(unittest.TestCase):

    def setUp(self):
        self.report = ReportCollector()
        self.plugin = ImputeMissingValuesPlugin(self.report)

    def test_execute_imputes_text_with_constant(self):
        df = pd.DataFrame({
            "city": [
                "Berlin",
                None,
                "Paris",
            ]
        })
        df.dg.config.imputation.enabled = True

        df.dg.config.imputation.text_strategy = "constant"
        df.dg.config.imputation.text_constant = "Unknown"

        result = self.plugin.run(df)

        expected = pd.DataFrame({
            "city": [
                "Berlin",
                "Unknown",
                "Paris",
            ]
        })

        assert_frame_equal(expected, result)

    def test_execute_imputes_category_with_constant(self):
        df = pd.DataFrame({
            "country": pd.Series(
                ["USA", None, "Canada"],
                dtype="category",
            )
        })
        df.dg.config.imputation.enabled = True

        df.dg.config.imputation.category_strategy = "constant"
        df.dg.config.imputation.category_constant = "Unknown"

        result = self.plugin.run(df)

        expected = pd.DataFrame({
            "country": pd.Series(
                ["USA", "Unknown", "Canada"],
                dtype="category",
            )
        })

        assert_frame_equal(expected, result)

    def test_execute_imputes_boolean_with_constant(self):
        df = pd.DataFrame({
            "approved": pd.Series(
                [True, None, False],
                dtype="boolean",
            )
        })
        df.dg.config.imputation.enabled = True

        df.dg.config.imputation.boolean_strategy = "constant"
        df.dg.config.imputation.boolean_constant = False

        result = self.plugin.run(df)

        expected = pd.DataFrame({
            "approved": pd.Series(
                [True, False, False],
                dtype="boolean",
            )
        })

        assert_frame_equal(expected, result)

    def test_execute_imputes_numeric_with_constant(self):
        df = pd.DataFrame({
            "age": [10, None, 30],
        })
        df.dg.config.imputation.enabled = True

        df.dg.config.imputation.numeric_strategy = "constant"
        df.dg.config.imputation.numeric_constant = -1

        result = self.plugin.run(df)

        expected = pd.DataFrame({
            "age": [10.0, -1.0, 30.0],
        })

        assert_frame_equal(expected, result)

    def test_execute_imputes_datetime_with_constant(self):
        df = pd.DataFrame({
            "date": pd.to_datetime([
                "2024-01-01",
                None,
                "2024-01-03",
            ])
        })
        df.dg.config.imputation.enabled = True

        df.dg.config.imputation.datetime_strategy = "constant"
        df.dg.config.imputation.datetime_constant = "2000-01-01"

        result = self.plugin.run(df)

        expected = pd.DataFrame({
            "date": pd.to_datetime([
                "2024-01-01",
                "2000-01-01",
                "2024-01-03",
            ])
        })

        assert_frame_equal(expected, result)

    def test_execute_datetime_backward_fill_preserves_trailing_missing(self):
        df = pd.DataFrame({
            "date": pd.to_datetime([
                "2024-01-01",
                None,
                None,
            ])
        })
        df.dg.config.imputation.enabled = True

        df.dg.config.imputation.datetime_strategy = "bfill"

        result = self.plugin.run(df)

        expected = pd.DataFrame({
            "date": pd.to_datetime([
                "2024-01-01",
                None,
                None,
            ])
        })

        assert_frame_equal(expected, result)

    def test_execute_datetime_forward_fill_preserves_leading_missing(self):
        df = pd.DataFrame({
            "date": pd.to_datetime([
                None,
                None,
                "2024-01-01",
            ])
        })
        df.dg.config.imputation.enabled = True

        result = self.plugin.run(df)

        expected = pd.DataFrame({
            "date": pd.to_datetime([
                None,
                None,
                "2024-01-01",
            ])
        })

        assert_frame_equal(expected, result)

    def test_execute_numeric_all_values_missing(self):
        df = pd.DataFrame({
            "age": [None, None],
        })
        df.dg.config.imputation.enabled = True

        result = self.plugin.run(df)

        expected = pd.DataFrame({
            "age": [None, None],
        })

        assert_frame_equal(expected, result)

    def test_execute_text_multiple_modes_uses_first_mode(self):
        df = pd.DataFrame({
            "city": [
                "Berlin",
                "Paris",
                None,
            ]
        })
        df.dg.config.imputation.enabled = True

        result = self.plugin.run(df)

        expected = pd.DataFrame({
            "city": [
                "Berlin",
                "Paris",
                "Berlin",
            ]
        })

        assert_frame_equal(expected, result)

    def test_execute_imputes_numeric_with_median(self):
        df = pd.DataFrame({
            "age": [10, None, 30],
        })
        df.dg.config.imputation.enabled = True

        result = self.plugin.run(df)

        expected = pd.DataFrame({
            "age": [10.0, 20.0, 30.0],
        })

        assert_frame_equal(expected, result)

        expected_data = {
            "imputation": {
                "ImputeMissingValuesPlugin": {
                    "age": {
                        "strategy": "median",
                        "filled": 1,
                    }
                }
            }
        }

        self.assertEqual(expected_data, self.report.data)

    def test_execute_imputes_category_with_mode(self):
        df = pd.DataFrame({
            "color": pd.Series(
                ["red", None, "red", "blue"],
                dtype="category",
            )
        })
        df.dg.config.imputation.enabled = True

        result = self.plugin.run(df)

        expected = pd.DataFrame({
            "color": pd.Series(
                ["red", "red", "red", "blue"],
                dtype="category",
            )
        })

        assert_frame_equal(expected, result)
        self.assertTrue(is_categorical_dtype(result["color"]))

    def test_execute_imputes_text_with_mode(self):
        df = pd.DataFrame({
            "city": [
                "Berlin",
                None,
                "Berlin",
                "Paris",
            ]
        })
        df.dg.config.imputation.enabled = True

        result = self.plugin.run(df)

        expected = pd.DataFrame({
            "city": [
                "Berlin",
                "Berlin",
                "Berlin",
                "Paris",
            ]
        })

        assert_frame_equal(expected, result)

    def test_execute_imputes_datetime_with_forward_fill(self):
        df = pd.DataFrame({
            "date": pd.to_datetime([
                "2024-01-01",
                None,
                "2024-01-03",
            ])
        })
        df.dg.config.imputation.enabled = True

        result = self.plugin.run(df)

        expected = pd.DataFrame({
            "date": pd.to_datetime([
                "2024-01-01",
                "2024-01-01",
                "2024-01-03",
            ])
        })

        assert_frame_equal(expected, result)

    def test_execute_imputes_boolean_with_mode(self):
        df = pd.DataFrame({
            "flag": pd.Series(
                [True, None, True, False],
                dtype="boolean",
            )
        })
        df.dg.config.imputation.enabled = True

        result = self.plugin.run(df)

        expected = pd.DataFrame({
            "flag": pd.Series(
                [True, True, True, False],
                dtype="boolean",
            )
        })

        assert_frame_equal(expected, result)

    def test_execute_respects_numeric_mean_strategy(self):
        df = pd.DataFrame({
            "age": [10, None, 40],
        })
        df.dg.config.imputation.enabled = True

        df.dg.config.imputation.numeric_strategy = "mean"

        result = self.plugin.run(df)

        expected = pd.DataFrame({
            "age": [10.0, 25.0, 40.0],
        })

        assert_frame_equal(expected, result)

    def test_execute_reports_no_missing_values(self):
        df = pd.DataFrame({
            "age": [10, 20, 30],
            "city": ["A", "B", "C"],
        })
        df.dg.config.imputation.enabled = True

        result = self.plugin.run(df)

        assert_frame_equal(df, result)

        expected_data = {
            "imputation": {
                "ImputeMissingValuesPlugin": {}
            }
        }

        self.assertEqual(expected_data, self.report.data)

        expected_report = {
            "imputation": {
                "ImputeMissingValuesPlugin":
                    "No missing values imputed."
            }
        }

        self.assertEqual(expected_report, self.report.report)

    def test_execute_reports_multiple_columns(self):
        df = pd.DataFrame({
            "age": [10, None, 30],
            "city": ["Berlin", None, "Berlin"],
        })
        df.dg.config.imputation.enabled = True

        self.plugin.run(df)

        expected_data = {
            "imputation": {
                "ImputeMissingValuesPlugin": {
                    "age": {
                        "strategy": "median",
                        "filled": 1,
                    },
                    "city": {
                        "strategy": "mode",
                        "filled": 1,
                    },
                }
            }
        }

        self.assertEqual(expected_data, self.report.data)

        expected_report = {'imputation': {'ImputeMissingValuesPlugin': 'Filled missing values:\n'
                                             '- age: median (1) (33.3%)\n'
                                             '- city: mode (1) (33.3%)'}}

        self.assertEqual(expected_report, self.report.report)


if __name__ == '__main__':
    unittest.main()
