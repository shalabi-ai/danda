from collections.abc import Sequence
import pandas as pd
from danda.plugins.optimization.information import DataFrameInformation
from danda.plugins.plugin import Plugin
from danda.plugins.report_collector import ReportCollector


class ChainPlugin(Plugin):
    def __init__(self, plugins: Sequence[Plugin], report: ReportCollector):
        super().__init__("ChainPlugin", "chain", report)

        self._plugins: list[Plugin] = []

        for plugin in plugins:
            self.add(plugin)

    def add(self, plugin: Plugin) -> None:
        if not isinstance(plugin, Plugin):
            raise TypeError(f"{plugin!r} is not a Plugin")
        self._plugins.append(plugin)
        return

    def _execute(self, df: pd.DataFrame, report: ReportCollector) -> pd.DataFrame:
        current_plugin: Plugin

        for plugin in self._plugins:
            try:
                current_plugin = plugin
                df = plugin.run(df, report)
            except Exception as exc:
                report.add_report("exception", current_plugin.plugin_name, str(exc))

        return df

    def _report(self, data, report: ReportCollector):
        return {
            "plugins_count": data["plugins_count"],
            "plugin_names": data["plugin_names"],
            "memory_usage": data["memory_usage"],
           # "result": deepcopy(self.chain_collector.report),
        }

    def _get_report_data(self, before: pd.DataFrame, after: pd.DataFrame, report: ReportCollector):
        return {
            "plugins_count": len(self._plugins),
            "plugin_names": [p.plugin_name for p in self._plugins],
            "memory_usage": DataFrameInformation.evaluate_memory_usage(before, after)
            #"result": deepcopy(self.chain_collector.data),
        }