import pandas as pd
from danda.plugins.clean.clean_plugin import CleanPlugin
from danda.plugins.report_collector import ReportCollector

class DropDuplicatesPlugin(CleanPlugin):
    def __init__(self, report: ReportCollector):
        super().__init__("DropDuplicates", report)

    def _execute(self, df: pd.DataFrame, report: ReportCollector) -> pd.DataFrame:
        config = self._get_config_params(df)
        ignore_index=config.get("ignore_index", False)
        return df.drop_duplicates(ignore_index=ignore_index) #ignore_index=True)

    def _report(self, data, report: ReportCollector) -> str:
        return f"Number of deleted rows: {data}"

    def _get_report_data(self, before: pd.DataFrame, after: pd.DataFrame, report: ReportCollector):
        return len(before) - len(after)

    def _get_config_params(self, df: pd.DataFrame) -> dict:
        config = self._get_config(df).cleaning
        return {
            "enabled": config.remove_duplicates,
            "ignore_index": config.remove_duplicates_ignore_index
        }
