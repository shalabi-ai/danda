import pandas as pd
from danda.plugins.clean.clean_plugin import CleanPlugin
from danda.plugins.report_collector import ReportCollector


class EmptyColumnsPlugin(CleanPlugin):
    def __init__(self, report: ReportCollector):
        super().__init__("EmptyColumnsPlugin", report)

    def _execute(self, df: pd.DataFrame, report: ReportCollector) -> pd.DataFrame:
        result =  df.dropna(axis=1, how="all")
        return result

    def _get_report_data(self, before: pd.DataFrame, after: pd.DataFrame, report: ReportCollector):
        return len(before.columns) - len(after.columns)

    def _report(self, data, report: ReportCollector) -> str:
        if data == 0:
            return "No empty columns deleted."
        return f'Number of deleted columns: {data}'

    def _get_config_params(self, df: pd.DataFrame) -> dict:
        config = self._get_config(df).cleaning
        return {
            "enabled": config.remove_empty_columns
        }

