import unittest

import pandas as pd
from danda.plugins.clean.drop_duplicates import DropDuplicatesPlugin
from danda.plugins.clean.empty_columns_plugin import EmptyColumnsPlugin
from danda.plugins.clean.empty_rows_plugin import EmptyRowsPlugin
from danda.plugins.clean.empty_spaces import EmptySpacesPlugin

from danda.plugins.report_collector import ReportCollector
import danda  # noqa: F401  # registers the pandas accessor
from pandas.testing import assert_frame_equal


class TestPluginEnabled(unittest.TestCase):
    def disable_plugins(self, df: pd.DataFrame):
        cleaning_config = self.df.dg.config.cleaning
        cleaning_config.remove_duplicates = False
        cleaning_config.remove_empty_rows = False
        cleaning_config.remove_empty_columns = False
        cleaning_config.strip_whitespace = False

    def setUp(self):
        self.df = pd.DataFrame({
            "boolean": ["True", "False", "True"],
            "numeric": ["1", "2", "3"],
            "datetime": ["2024-01-01", "2024-01-02", "2024-01-03"],
            "category": ["A", "A", "B"],
        })
        self.disable_plugins(self.df)
        report = ReportCollector()

        self.plugins = [
            DropDuplicatesPlugin(report),
            EmptyColumnsPlugin(report),
            EmptyRowsPlugin(report),
            EmptySpacesPlugin(report),
        ]

    def test_plugin_disabled(self):
        for plugin in self.plugins:
            result = plugin.run(self.df)
            assert_frame_equal(result, self.df)


if __name__ == '__main__':
    unittest.main()
