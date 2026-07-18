import pandas as pd
from danda.plugins.clean.clean_plugin import CleanPlugin
from danda.plugins.report_collector import ReportCollector


class EmptyRowsPlugin(CleanPlugin):
    def __init__(self, report: ReportCollector):
        super().__init__("EmptyRowsPlugin", report)

    def _execute(self, df: pd.DataFrame, report: ReportCollector) -> pd.DataFrame:
        return df.dropna(how="all")

    def _report(self, data, report: ReportCollector) -> str:
        if data == 0:
            return "No empty rows deleted."
        return f"Number of deleted rows: {data}"

    def _get_report_data(self, before: pd.DataFrame, after: pd.DataFrame, report: ReportCollector):
        return before.index.size - after.index.size

    def _get_config_params(self, df: pd.DataFrame) -> dict:
        config = self._get_config(df).cleaning
        return {
            "enabled": config.remove_empty_rows
        }