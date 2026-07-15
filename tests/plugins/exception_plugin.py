import pandas as pd

from danda.plugins.plugin import Plugin
from danda.plugins.report_collector import ReportCollector


class ExceptionPlugin(Plugin):
    name: str = "ExceptionPlugin"

    def __init__(self, report: ReportCollector):
        super().__init__(ExceptionPlugin.name, "ExceptionCategory", report)
        self._counter = 0

    def _execute(self, df: pd.DataFrame, report: ReportCollector) -> pd.DataFrame:
        raise
        return df

    def _get_report_data(self, before: pd.DataFrame, after: pd.DataFrame, report: ReportCollector):
        return 0

    def _report(self, data, report: ReportCollector) -> str:
        return ""
