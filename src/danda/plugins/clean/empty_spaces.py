import pandas as pd
from danda.plugins.clean.clean_plugin import CleanPlugin
from danda.plugins.optimization.information import DataFrameInformation
from danda.plugins.plugin import Plugin
from danda.plugins.report_collector import ReportCollector

class EmptySpacesPlugin(CleanPlugin):
    def __init__(self, report: ReportCollector):
        super().__init__("EmptySpacesPlugin", report)

    def _execute(self, df: pd.DataFrame, report: ReportCollector) -> pd.DataFrame:
        result = df.copy()

        string_columns = DataFrameInformation.get_string_columns(df)
        result[string_columns] = result[string_columns].apply(
            lambda s: s.str.strip()
        )

        return result

    def _get_report_data(self, before: pd.DataFrame, after: pd.DataFrame, report: ReportCollector):
        changed = []

        for col in DataFrameInformation.get_string_columns(before):
            if not before[col].equals(after[col]):
                changed.append(col)

        return changed

    def _report(self, data, report: ReportCollector) -> str:
        if not data:
            return "No leading or trailing whitespace found."

        return f"Stripped leading/trailing whitespace from columns: {', '.join(data)}"
