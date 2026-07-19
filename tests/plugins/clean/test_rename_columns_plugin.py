import unittest

import pandas as pd
from pandas.testing import assert_frame_equal

import danda  # noqa: F401
from danda.configuration.clean_configuration import ColumnCase
from danda.plugins.clean.rename_columns_plugin import RenameColumnsPlugin

from danda.plugins.report_collector import ReportCollector


class TestRenameColumnsPlugin(unittest.TestCase):

    def setUp(self):
        self.report = ReportCollector()
        self.plugin = RenameColumnsPlugin(self.report)

    def test_execute_renames_columns_to_snake_case(self):
        df = pd.DataFrame(
            {
                "Customer Name": ["Alice"],
                "Order-Date": [100],
                "Total.Price": [10.5],
            }
        )

        df.dg.config.cleaning.rename_column_enabled = True
        df.dg.config.cleaning.rename_column_style = ColumnCase.SNAKE

        result = self.plugin.run(df)

        expected = pd.DataFrame(
            {
                "customer_name": ["Alice"],
                "order_date": [100],
                "total_price": [10.5],
            }
        )

        assert_frame_equal(result, expected)

        expected_data = {
            "clean": {
                "RenameColumnsPlugin": {
                    "count": 3,
                    "renamed": {
                        "Customer Name": "customer_name",
                        "Order-Date": "order_date",
                        "Total.Price": "total_price",
                    },
                }
            }
        }

        self.assertEqual(expected_data, self.report.data)

        expected_report = {'clean': {'RenameColumnsPlugin': 'Renamed 3 column(s). columns: customer_name, order_date, total_price'}}

        self.assertEqual(expected_report, self.report.report)

    def test_execute_renames_columns_to_camel_case(self):
        df = pd.DataFrame(
            {
                "Customer Name": ["Alice"],
                "Order Date": [1],
                "date":["my date"]
            }
        )

        df.dg.config.cleaning.rename_column_enabled = True
        df.dg.config.cleaning.rename_column_style = ColumnCase.CAMEL

        result = self.plugin.run(df)

        self.assertListEqual(
            list(result.columns),
            ["customerName", "orderDate"],
        )

    def test_execute_renames_columns_to_lower(self):
        df = pd.DataFrame(
            {
                "Customer Name": ["Alice"],
                "TOTAL": [1],
            }
        )

        df.dg.config.cleaning.rename_column_enabled = True
        df.dg.config.cleaning.rename_column_style = ColumnCase.LOWER

        result = self.plugin.run(df)

        self.assertListEqual(
            list(result.columns),
            ["customer name", "total"],
        )

    def test_execute_no_columns_changed(self):
        df = pd.DataFrame(
            {
                "customer_name": ["Alice"],
                "order_date": [1],
            }
        )

        df.dg.config.cleaning.rename_column_enabled = True
        df.dg.config.cleaning.rename_column_style = ColumnCase.SNAKE

        result = self.plugin.run(df)

        assert_frame_equal(result, df)

        expected_data = {
            "clean": {
                "RenameColumnsPlugin": {
                    "count": 0,
                    "renamed": {},
                }
            }
        }

        self.assertEqual(expected_data, self.report.data)

        expected_report = {
            "clean": {
                "RenameColumnsPlugin": "No columns were renamed."
            }
        }

        self.assertEqual(expected_report, self.report.report)

    def test_original_dataframe_is_not_modified(self):
        df = pd.DataFrame(
            {
                "Customer Name": ["Alice"],
            }
        )

        original = df.copy(deep=True)

        df.dg.config.cleaning.rename_column_enabled = True
        df.dg.config.cleaning.rename_column_style = ColumnCase.SNAKE

        self.plugin.run(df)

        assert_frame_equal(df, original)
        self.assertListEqual(list(df.columns), ["Customer Name"])

if __name__ == '__main__':
    unittest.main()
