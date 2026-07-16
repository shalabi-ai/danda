import pandas as pd
from danda.plugins.clean.clean_plugin import CleanPlugin
from danda.plugins.report_collector import ReportCollector


class EmptyRowsPlugin(CleanPlugin):
    def __init__(self, report: ReportCollector):
        super().__init__("EmptyRowsPlugin", report)

    def _execute(self, df: pd.DataFrame, report: ReportCollector) -> pd.DataFrame:
        return df.dropna(how="all")

    def _report(self, data, report: ReportCollector) -> str:
        return f"Number of deleted rows: {data}"

    def _get_report_data(self, before: pd.DataFrame, after: pd.DataFrame, report: ReportCollector):
        return before.index.size - after.index.size