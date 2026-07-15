import unittest
import pandas as pd
from danda.plugins.chain import ChainPlugin
from danda.plugins.report_collector import ReportCollector
from tests.plugins.counter_plugin import CounterPlugin
from tests.plugins.exception_plugin import ExceptionPlugin


class ChainPluginTestCase(unittest.TestCase):
    def test_add_valid_plugins(self):
        report_collector = ReportCollector()
        chain = ChainPlugin([], report_collector)
        collector = ReportCollector()
        counter_plugin = CounterPlugin(collector)
        chain.add(counter_plugin)
        chain.run(pd.DataFrame())
        self.assertEqual(counter_plugin.get_count(), 1)

        expected_data = {'chain': {'ChainPlugin': {'data': {'CounterCategory': {'CounterPlugin': 1}}, 'plugins': 1}}}
        self.assertEqual(expected_data, report_collector.data)

        expected_report = {'chain': {'ChainPlugin': "Number of plugins: 1\n report: {'CounterCategory': {'CounterPlugin': 'count: 1'}}"}}
        self.assertEqual(expected_report, report_collector.report)

        # counter plugin report should not be touched
        self.assertEqual({}, collector.data)
        self.assertEqual({}, collector.report)

    def test_exception_plugin(self):
        report_collector = ReportCollector()
        chain = ChainPlugin([ExceptionPlugin(report_collector)], report_collector)
        chain.run(pd.DataFrame())

        expected_data = {'chain': {'ChainPlugin': {'data': {}, 'plugins': 1}}}
        self.assertEqual(expected_data, report_collector.data)

        expected_report = {'chain': {'ChainPlugin': "Number of plugins: 1\n report: {'exception': {'ExceptionPlugin': 'No active exception to reraise'}}"}}
        self.assertEqual(expected_report, report_collector.report)

    def test_exception_counter_plugin(self):
        report_collector = ReportCollector()
        chain = ChainPlugin([ExceptionPlugin(report_collector), CounterPlugin(report_collector)], report_collector)
        chain.run(pd.DataFrame())

        expected_data = {'chain': {'ChainPlugin': {'data': {'CounterCategory': {'CounterPlugin': 1}}, 'plugins': 2}}}
        self.assertEqual(expected_data, report_collector.data)

        expected_report = {'chain': {'ChainPlugin': "Number of plugins: 2\n report: {'exception': {'ExceptionPlugin': 'No active exception to reraise'}, 'CounterCategory': {'CounterPlugin': 'count: 1'}}"}}
        self.assertEqual(expected_report, report_collector.report)

    def test_add_invalid_plugins(self):
        report_collector = ReportCollector()
        chain = ChainPlugin([], report_collector)
        with self.assertRaises(TypeError):
            chain.add(5)

    def test_invalid_constructor_plugins(self):
        report_collector = ReportCollector()
        counter_plugin = CounterPlugin(report_collector)
        with self.assertRaises(TypeError):
            ChainPlugin([counter_plugin, 6, counter_plugin], report_collector)

    def test_execute_with_constructor(self):
        report_collector = ReportCollector()
        counter_plugin = CounterPlugin(report_collector)
        data_frame = pd.DataFrame()
        chain = ChainPlugin([counter_plugin, counter_plugin, counter_plugin], report_collector)
        chain.run(data_frame)
        self.assertEqual(counter_plugin.get_count(), 3)

        expected_data ={'chain': {'ChainPlugin': {'data': {'CounterCategory': {'CounterPlugin': 1, 'CounterPlugin_2': 2, 'CounterPlugin_3': 3}}, 'plugins': 3}}}
        self.assertEqual(expected_data, report_collector.data)

        expected_report = {'chain': {'ChainPlugin': "Number of plugins: 3\n report: {'CounterCategory': {'CounterPlugin': 'count: 1', 'CounterPlugin_2': 'count: 2', 'CounterPlugin_3': 'count: 3'}}"}}
        self.assertEqual(expected_report, report_collector.report)

    def test_execute_empty_chain(self):
        report_collector = ReportCollector()
        df = pd.DataFrame({"a": [1]})
        chain = ChainPlugin([], report_collector)
        result = chain.run(df)

        self.assertIs(result, df)

    def test_execute_with_constructor_and_add(self):
        report_collector = ReportCollector()
        counter_plugin = CounterPlugin(None)
        data_frame =pd.DataFrame()
        chain = ChainPlugin([counter_plugin, counter_plugin, counter_plugin], report_collector)

        counter_add_plugin = CounterPlugin(None)
        chain.add(counter_add_plugin)
        chain.add(counter_add_plugin)

        chain.run(data_frame)

        self.assertEqual(counter_plugin.get_count(), 3)
        self.assertEqual(counter_add_plugin.get_count(), 2)

    def test_execute_returns_dataframe(self):
        report_collector = ReportCollector()
        df = pd.DataFrame({"a": [1]})
        chain = ChainPlugin([], report_collector)
        result = chain.run(df)

        self.assertIs(result, df)

if __name__ == '__main__':
    unittest.main()
