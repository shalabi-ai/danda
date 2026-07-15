from collections.abc import Sequence
import pandas as pd
from danda.plugins.plugin import Plugin
from copy import deepcopy

from danda.plugins.report_collector import ReportCollector


class ChainPlugin(Plugin):
    def __init__(self, plugins: Sequence[Plugin], report: ReportCollector):
        super().__init__("ChainPlugin", "chain", report)

        self.chain_collector = ReportCollector()

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
                df = plugin.run(df, self.chain_collector)
            except Exception as exc:
                self.chain_collector.add_report("exception", current_plugin.plugin_name, str(exc))

        return df

    def _report(self, data, report: ReportCollector) -> str:
        return  f"Number of plugins: {len(self._plugins)}\n report: {self.chain_collector.report}"

    def _get_report_data(self, before: pd.DataFrame, after: pd.DataFrame, report: ReportCollector):
        return {
            "plugins": len(self._plugins),
            "data": deepcopy(self.chain_collector.data),
        }