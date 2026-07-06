import unittest

import pandas as pd

from danda.plugins.chain import ChainPlugin
from tests.plugins.counter_plugin import CounterPlugin


class ChainPluginTestCase(unittest.TestCase):
    def test_add_valid_plugins(self):
        chain = ChainPlugin([])
        counter_plugin = CounterPlugin()
        chain.add(counter_plugin)
        chain.execute(pd.DataFrame())
        self.assertEqual(counter_plugin.get_count(), 1)

    def test_add_invalid_plugins(self):
        chain = ChainPlugin([])
        with self.assertRaises(TypeError):
            chain.add(5)

    def test_invalid_constructor_plugins(self):
        counter_plugin = CounterPlugin()
        with self.assertRaises(TypeError):
            ChainPlugin([counter_plugin, 6, counter_plugin])

    def test_execute_with_constructor(self):
        counter_plugin = CounterPlugin()
        data_frame = pd.DataFrame()
        chain = ChainPlugin([counter_plugin, counter_plugin, counter_plugin])
        chain.execute(data_frame)
        self.assertEqual(counter_plugin.get_count(), 3)

    def test_execute_empty_chain(self):
        df = pd.DataFrame({"a": [1]})
        chain = ChainPlugin([])
        result = chain.execute(df)

        self.assertIs(result, df)

    def test_execute_with_constructor_and_add(self):
        counter_plugin = CounterPlugin()
        data_frame =pd.DataFrame()
        chain = ChainPlugin([counter_plugin, counter_plugin, counter_plugin])

        counter_add_plugin = CounterPlugin()
        chain.add(counter_add_plugin)
        chain.add(counter_add_plugin)

        chain.execute(data_frame)

        self.assertEqual(counter_plugin.get_count(), 3)
        self.assertEqual(counter_add_plugin.get_count(), 2)

    def test_execute_returns_dataframe(self):
        df = pd.DataFrame({"a": [1]})
        chain = ChainPlugin([])
        result = chain.execute(df)

        self.assertIs(result, df)

if __name__ == '__main__':
    unittest.main()
