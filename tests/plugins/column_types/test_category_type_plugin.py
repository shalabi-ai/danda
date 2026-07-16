import unittest
import pandas as pd
from danda.plugins.column_types.category_type_plugin import CategoryTypePlugin
from danda.plugins.report_collector import ReportCollector
from pandas.api.types import is_categorical_dtype
from pandas.testing import assert_frame_equal
import danda # noqa: F401  # registers the pandas accessor


class TestCategoryTypePlugin(unittest.TestCase):

    def setUp(self):
        self.report = ReportCollector()
        self.plugin = CategoryTypePlugin(self.report)

    def test_execute_converts_category_columns(self):
        df = pd.DataFrame({
            "category": ["A"] * 95 + ["B"] * 5,
            "text": [f"value_{i}" for i in range(100)]
        })

        result = self.plugin.run(df)

        self.assertTrue(is_categorical_dtype(result["category"]))
        self.assertFalse(is_categorical_dtype(result["text"]))

        expected_data = {'types': {'CategoryTypePlugin': ['category']}}
        self.assertEqual(expected_data, self.report.data)

        expected_report = {'types': {'CategoryTypePlugin': 'Converted the following columns to category: category'}}
        self.assertEqual(expected_report, self.report.report)

    def test_find_category_columns(self):
        df = pd.DataFrame({
            "category": ["A"] * 95 + ["B"] * 5,
            "category2": ["X"] * 50 + ["Y"] * 50,
            "text": [f"value_{i}" for i in range(100)]
        })

        self.plugin.run(df)

        expected_data = {'types': {'CategoryTypePlugin': ['category', 'category2']}}
        self.assertEqual(expected_data, self.report.data)

        expected_report = {'types': {'CategoryTypePlugin': 'Converted the following columns to category: category, category2'}}
        self.assertEqual(expected_report, self.report.report)

    def test_no_category_columns(self):
        df = pd.DataFrame({
            "text": [f"value_{i}" for i in range(100)]
        })

        result = self.plugin.run(df)

        assert_frame_equal(result, df)

        expected_data = {'types': {'CategoryTypePlugin': []}}
        self.assertEqual(expected_data, self.report.data)

        expected_report = {'types': {'CategoryTypePlugin': 'No category columns detected.'}}
        self.assertEqual(expected_report, self.report.report)

    def test_skip_boolean_datetime_and_existing_category_columns(self):
        df = pd.DataFrame({
            "boolean": pd.Series(
                [True, False] * 50,
                dtype="boolean"
            ),
            "datetime": pd.Series(
                [pd.Timestamp("2024-01-01")] * 95 +
                [pd.Timestamp("2024-01-02")] * 5
            ),
            "category": pd.Series(
                ["A"] * 95 + ["B"] * 5,
                dtype="category"
            ),
            "text_category": ["X"] * 95 + ["Y"] * 5,
        })

        result = self.plugin._find_category_columns(df)

        self.assertEqual(result, ["text_category"])

        self.plugin.run(df)

        expected_data = {'types': {'CategoryTypePlugin': ['text_category']}}
        self.assertEqual(expected_data, self.report.data)

        expected_report = {'types': {'CategoryTypePlugin': 'Converted the following columns to category: text_category'}}
        self.assertEqual(expected_report, self.report.report)

    def test_threshold(self):
        df = pd.DataFrame({
            "col": [f"value_{i % 11}" for i in range(100)]
        })

        # 11 unique values / 100 rows = 11%
        self.assertEqual(
            self.plugin._find_category_columns(df, threshold=0.10),
            []
        )

        self.assertEqual(
            self.plugin._find_category_columns(df, threshold=0.11),
            ["col"]
        )

    def test_empty_dataframe(self):
        df = pd.DataFrame()

        self.assertEqual(
            self.plugin._find_category_columns(df),
            []
        )

    def test_all_unique_column(self):
        df = pd.DataFrame({
            "id": range(100)
        })

        self.assertEqual(
            self.plugin._find_category_columns(df),
            []
        )

    def test_handles_missing_values(self):
        df = pd.DataFrame({
            "status": (
                    ["Open"] * 45 +
                    ["Closed"] * 45 +
                    [None] * 10
            )
        })

        result = self.plugin.run(df, self.report)

        self.assertTrue(is_categorical_dtype(result["status"]))


    def test_execute_preserves_values(self):
        df = pd.DataFrame({
            "category": ["A"] * 95 + ["B"] * 5
        })

        result = self.plugin.run(df)

        expected = df.copy()
        expected["category"] = expected["category"].astype("category")

        assert_frame_equal(result, expected)

    def test_category_threshold_configuration(self):
        # 8 unique values / 100 rows = 0.08 unique ratio
        df = pd.DataFrame({
            "category": [f"value_{i % 8}" for i in range(100)]
        })

        plugin = CategoryTypePlugin(ReportCollector())
        result = plugin.run(df)

        # Should remain object because 0.08 > 0.05
        self.assertEqual(result["category"].dtype, "category")

        df.dg.config.types.category_threshold = 0.05

        plugin = CategoryTypePlugin(ReportCollector())
        result = plugin.run(df)

        # Should remain object because 0.08 > 0.05
        self.assertNotEqual(result["category"].dtype, "category")


if __name__ == "__main__":
    unittest.main()