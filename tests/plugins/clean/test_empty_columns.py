import unittest

import pandas as pd
import numpy as np
from danda.plugins.clean.empty_columns_plugin import EmptyColumnsPlugin
from danda.plugins.report_collector import ReportCollector
from pandas.testing import assert_frame_equal


class EmptyRowsTestCase(unittest.TestCase):
    def test_empty_columns(self):
        data = pd.DataFrame({
            "A": [1, 2, 3],
            "B": [np.nan, np.nan, np.nan],  # Entirely empty
            "C": [4, np.nan, 6],
            "D": [np.nan, np.nan, np.nan],  # Entirely empty
        })

        report = ReportCollector()
        plugin = EmptyColumnsPlugin(report)
        result = plugin.run(data)

        expected = pd.DataFrame({
            "A": [1, 2, 3],
            "C": [4, np.nan, 6],
        })

        assert_frame_equal(result, expected)

        expected_data = {'clean': {'EmptyColumnsPlugin': 2}}
        self.assertEqual(expected_data, report.data)

        expected_report = {'clean': {'EmptyColumnsPlugin': 'Number of deleted columns: 2'}}
        self.assertEqual(expected_report, report.report)

    def test_all_empty_columns(self):
        data = pd.DataFrame({
            "A": [np.nan, np.nan],
            "B": [np.nan, np.nan],
        })

        report = ReportCollector()
        plugin = EmptyColumnsPlugin(report)
        result = plugin.run(data)


        self.assertEqual(len(result.columns), 0)

        expected_data = {'clean': {'EmptyColumnsPlugin': 2}}
        self.assertEqual(expected_data, report.data)

        expected_report = {'clean': {'EmptyColumnsPlugin': 'Number of deleted columns: 2'}}
        self.assertEqual(expected_report, report.report)

if __name__ == '__main__':
    unittest.main()
