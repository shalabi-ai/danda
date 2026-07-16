import unittest

import pandas as pd
from danda.plugins.column_types.boolean_type_plugin import BooleanTypePlugin
from danda.plugins.column_types.category_type_plugin import CategoryTypePlugin
from danda.plugins.column_types.datetime_type_plugin import DateTimeTypePlugin
from danda.plugins.column_types.numeric_type_plugin import NumericTypePlugin

from danda.plugins.report_collector import ReportCollector
import danda  # noqa: F401  # registers the pandas accessor
from pandas.testing import assert_frame_equal


class TestPluginEnabled(unittest.TestCase):
    def disable_plugins(self, df: pd.DataFrame):
        types_config = self.df.dg.config.types
        types_config.boolean_enabled = False
        types_config.datetime_enabled = False
        types_config.numeric_enabled = False
        types_config.category_enabled = False

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
            BooleanTypePlugin(report),
            NumericTypePlugin(report),
            DateTimeTypePlugin(report),
            CategoryTypePlugin(report),
        ]

    def test_plugin_disabled(self):
        for plugin in self.plugins:
            result = plugin.run(self.df)
            assert_frame_equal(result, self.df)


if __name__ == '__main__':
    unittest.main()
