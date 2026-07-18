import unittest

import pandas as pd
import pandas.testing as pdt
import danda # noqa: F401  # registers the pandas accessor


class TestHandleOutliers(unittest.TestCase):

    def test_no_columns_returns_original_dataframe(self):
        df = pd.DataFrame({
            "Age": [20, 21, 100],
        })

        result = df.dg.action.handle_outliers()

        pdt.assert_frame_equal(result, df)

    def test_empty_columns_returns_original_dataframe(self):
        df = pd.DataFrame({
            "Age": [20, 21, 100],
        })

        result = df.dg.action.handle_outliers(columns=[])

        pdt.assert_frame_equal(result, df)

    def test_remove_outliers(self):
        df = pd.DataFrame({
            "Age": [10] * 20 + [100],
        })

        result = df.dg.action.handle_outliers(
            columns=["Age"],
            strategy="remove",
        )

        self.assertEqual(len(result), 20)
        self.assertNotIn(100, result["Age"].values)

    def test_replace_outliers_with_nan(self):
        df = pd.DataFrame({
            "Age": [10] * 20 + [100],
        })

        result = df.dg.action.handle_outliers(
            columns=["Age"],
            strategy="nan",
        )

        self.assertEqual(result["Age"].isna().sum(), 1)
        self.assertEqual(len(result), len(df))

    def test_clip_outliers(self):
        df = pd.DataFrame({
            "Age": [10] * 20 + [100],
        })

        result = df.dg.action.handle_outliers(
            columns=["Age"],
            strategy="clip",
        )

        self.assertEqual(len(result), len(df))
        self.assertLess(result["Age"].max(), 100)

    def test_only_selected_columns_are_modified(self):
        df = pd.DataFrame({
            "Age": [10] * 20 + [100],
            "Fare": [1] * 20 + [999],
        })

        result = df.dg.action.handle_outliers(
            columns=["Age"],
            strategy="nan",
        )

        self.assertEqual(result["Age"].isna().sum(), 1)
        self.assertEqual(result["Fare"].isna().sum(), 0)
        self.assertEqual(result["Fare"].iloc[-1], 999)

    def test_invalid_column_raises_key_error(self):
        df = pd.DataFrame({
            "Age": [1, 2, 3],
        })

        with self.assertRaises(KeyError):
            df.dg.action.handle_outliers(
                columns=["Salary"],
            )

    def test_non_numeric_column_raises_type_error(self):
        df = pd.DataFrame({
            "Name": ["Alice", "Bob", "Charlie"],
        })

        with self.assertRaises(TypeError):
            df.dg.action.handle_outliers(
                columns=["Name"],
            )

    def test_invalid_strategy_raises_value_error(self):
        df = pd.DataFrame({
            "Age": [10] * 20 + [100],
        })

        with self.assertRaises(ValueError):
            df.dg.action.handle_outliers(
                columns=["Age"],
                strategy="invalid",
            )

    def test_constant_column_is_unchanged(self):
        df = pd.DataFrame({
            "Age": [10] * 20,
        })

        result = df.dg.action.handle_outliers(
            columns=["Age"],
            strategy="remove",
        )

        pdt.assert_frame_equal(result, df)

    def test_missing_values_are_preserved(self):
        df = pd.DataFrame({
            "Age": [10] * 20 + [100, None],
        })

        result = df.dg.action.handle_outliers(
            columns=["Age"],
            strategy="nan",
        )

        self.assertEqual(result["Age"].isna().sum(), 2)

if __name__ == '__main__':
    unittest.main()