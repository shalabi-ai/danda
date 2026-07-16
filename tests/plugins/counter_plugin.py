import pandas as pd

from danda.plugins.plugin import Plugin
from danda.plugins.report_collector import ReportCollector


class CounterPlugin(Plugin):
    name: str = "CounterPlugin"

    def __init__(self, report: ReportCollector):
        super().__init__(CounterPlugin.name, "CounterCategory", report)
        self._counter = 0

    def _execute(self, df: pd.DataFrame, report: ReportCollector) -> pd.DataFrame:
        self._counter += 1
        return df

    def _get_report_data(self, before: pd.DataFrame, after: pd.DataFrame, report: ReportCollector):
        return self.get_count()

    def _report(self, data, report: ReportCollector) -> str:
        return f"count: {self.get_count()}"

    def get_count(self)->int:
        return self._counter

    def _get_config_params(self, df: pd.DataFrame) -> dict:
        return {
            "enabled" : True
        }