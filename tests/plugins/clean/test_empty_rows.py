import unittest

import pandas as pd
import numpy as np
from danda.plugins.clean.empty_rows_plugin import EmptyRowsPlugin
from danda.plugins.report_collector import ReportCollector
from pandas.testing import assert_frame_equal


class EmptyRowsTestCase(unittest.TestCase):
    def test_empty_rows(self):
        data = pd.DataFrame({
            "Name": ["Alice", np.nan, "Charlie", np.nan, "Eve"],
            "Age": [25, np.nan, np.nan, np.nan, 30],
            "City": ["New York", np.nan, "Chicago", np.nan, np.nan],
        })

        report = ReportCollector()

        plugin = EmptyRowsPlugin(report)
        result = plugin.run(data)

        expected = pd.DataFrame({
            "Name": ["Alice", "Charlie", "Eve"],
            "Age": [25.0, np.nan, 30.0],
            "City": ["New York", "Chicago", np.nan],
        }, index=[0, 2, 4])

        assert_frame_equal(result, expected) # add assertion here

        expected_data = {'clean': {'EmptyRowsPlugin': 2}}
        self.assertEqual(expected_data, report.data)

        expected_report = {'clean': {'EmptyRowsPlugin': 'Number of deleted rows: 2'}}
        self.assertEqual(expected_report, report.report)

    def test_no_empty_rows(self):
        data = pd.DataFrame({
            "Name": ["Alice", np.nan, "Charlie", np.nan, "Eve"],
            "Age": [25, np.nan, np.nan, 7, 30],
            "City": ["New York", "test", "Chicago", np.nan, np.nan]
        })

        report = ReportCollector()
        plugin = EmptyRowsPlugin(report)
        new_data = plugin.run(data)
        self.assertEqual(new_data.size, data.size)

        expected_data = {'clean': {'EmptyRowsPlugin': 0}}
        self.assertEqual(expected_data, report.data)

        expected_report = {'clean': {'EmptyRowsPlugin': 'No empty rows deleted.'}}
        self.assertEqual(expected_report, report.report)

if __name__ == '__main__':
    unittest.main()
