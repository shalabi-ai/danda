import unittest

import pandas as pd
from danda.plugins.column_types.datetime_type_plugin import DateTimeTypePlugin
from danda.plugins.report_collector import ReportCollector
from pandas.testing import assert_frame_equal
from pandas.api.types import is_datetime64_any_dtype

class TestDateTimeTypePlugin(unittest.TestCase):

    def setUp(self):
        self.report = ReportCollector()
        self.plugin = DateTimeTypePlugin(self.report)

    def test_execute_converts_datetime_columns(self):
        df = pd.DataFrame({
            "created": [
                "2024-01-01",
                "2024-01-02",
                "2024-01-03"
            ],
            "name": [
                "Alice",
                "Bob",
                "Charlie"
            ]
        })

        result = self.plugin.run(df)

        self.assertTrue(is_datetime64_any_dtype(result["created"]))

        expected_data = {'types': {'DateTimeTypePlugin': ['created']}}
        self.assertEqual(expected_data, self.report.data)

        expected_report = {'types': {'DateTimeTypePlugin': 'Converted the following columns to datetime: created'}}
        self.assertEqual(expected_report, self.report.report)

    def test_execute_preserves_non_datetime_columns(self):
        df = pd.DataFrame({
            "city": ["London", "Paris", "Berlin"],
            "age": [20, 30, 40]
        })

        result = self.plugin.run(df)

        assert_frame_equal(result, df)

        expected_data = {'types': {'DateTimeTypePlugin': []}}
        self.assertEqual(expected_data, self.report.data)

        expected_report = {'types': {'DateTimeTypePlugin': 'No datetime columns detected.'}}
        self.assertEqual(expected_report, self.report.report)

    def test_find_datetime_columns(self):
        df = pd.DataFrame({
            "created": [
                "2024-01-01",
                "2024-01-02",
                "2024-01-03"
            ],
            "updated": [
                "2024/02/01",
                "2024/02/02",
                "2024/02/03"
            ],
            "name": [
                "Alice",
                "Bob",
                "Charlie"
            ]
        })

        self.plugin.run(df)

        expected_data = {'types': {'DateTimeTypePlugin': ['created', 'updated']}}
        self.assertEqual(expected_data, self.report.data)

        expected_report = {'types': {'DateTimeTypePlugin': 'Converted the following columns to datetime: created, updated'}}
        self.assertEqual(expected_report, self.report.report)

    def test_all_date_values(self):
        df = pd.DataFrame({
            "iso_date": [
                "2024-01-01",
                "2024-01-02",
                "2024-01-03",
            ],
            "slash_date": [
                "2024/01/01",
                "2024/01/02",
                "2024/01/03",
            ],
            "date_time": [
                "2024-01-01 12:34:56",
                "2024-01-02 13:45:10",
                "2024-01-03 14:56:20",
            ],
            "iso_datetime": [
                "2024-01-01T12:34:56",
                "2024-01-02T13:45:10",
                "2024-01-03T14:56:20",
            ],
            "utc_datetime": [
                "2024-01-01T12:34:56Z",
                "2024-01-02T13:45:10Z",
                "2024-01-03T14:56:20Z",
            ],
            "offset_datetime": [
                "2024-01-01T12:34:56+01:00",
                "2024-01-02T13:45:10+01:00",
                "2024-01-03T14:56:20+01:00",
            ],
            "microseconds": [
                "2024-01-01 12:34:56.123456",
                "2024-01-02 13:45:10.654321",
                "2024-01-03 14:56:20.999999",
            ],
            "month_name_short": [
                "Jan 01, 2024",
                "Feb 02, 2024",
                "Mar 03, 2024",
            ],
            "month_name_long": [
                "January 01, 2024",
                "February 02, 2024",
                "March 03, 2024",
            ],
            "day_month_name": [
                "01 Jan 2024",
                "02 Feb 2024",
                "03 Mar 2024",
            ],
            "compact_iso": [
                "20240101",
                "20240202",
                "20240303",
            ],
            "not_datetime": [
                "Alice",
                "Bob",
                "Charlie",
            ],
        })


        self.plugin.run(df)

        expected_data = {'types': {'DateTimeTypePlugin': ['iso_date', 'slash_date', 'date_time', 'iso_datetime', 'utc_datetime', 'offset_datetime', 'microseconds', 'month_name_short', 'month_name_long', 'day_month_name', 'compact_iso']}}
        self.assertEqual(expected_data, self.report.data)

        expected_report = {'types': {'DateTimeTypePlugin': 'Converted the following columns to datetime: iso_date, slash_date, date_time, iso_datetime, utc_datetime, offset_datetime, microseconds, month_name_short, month_name_long, day_month_name, compact_iso'}}
        self.assertEqual(expected_report, self.report.report)

    def test_handles_missing_values(self):
        df = pd.DataFrame({
            "created": [
                "2024-01-01",
                None,
                "2024-01-03"
            ]
        })

        result = self.plugin.run(df)

        self.assertTrue(is_datetime64_any_dtype(result["created"]))
        self.assertTrue(pd.isna(result.loc[1, "created"]))

        expected_data = {'types': {'DateTimeTypePlugin': ['created']}}
        self.assertEqual(expected_data, self.report.data)

        expected_report = {'types': {'DateTimeTypePlugin': 'Converted the following columns to datetime: created'}}
        self.assertEqual(expected_report, self.report.report)

    def test_success_threshold(self):
        df = pd.DataFrame({
            "dates": [
                "2024-01-01",
                "not a date",
                "2024-01-03",
                "2024-01-04"
            ]
        })

        result = self.plugin._find_datetime_columns(
            df,
            success_threshold=0.75
        )

        self.assertEqual(result, ["dates"])

        result = self.plugin._find_datetime_columns(
            df,
            success_threshold=1.0
        )

        self.assertEqual(result, [])



if __name__ == "__main__":
    unittest.main()
