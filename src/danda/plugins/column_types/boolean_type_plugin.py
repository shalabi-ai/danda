import pandas as pd

from danda.plugins.column_types.column_type_identification import ColumnTypeIdentification
from danda.plugins.column_types.type_plugin import TypePlugin
from danda.plugins.report_collector import ReportCollector


class BooleanTypePlugin(TypePlugin):
    _mapping = {
        True: True,
        False: False,
        1: True,
        0: False,
        "1": True,
        "0": False,
        "true": True,
        "false": False,
        "True": True,
        "False": False,
    }

    def __init__(self, report: ReportCollector):
        super().__init__("BooleanTypePlugin", report)

    def _execute(self, df: pd.DataFrame, report: ReportCollector) -> pd.DataFrame:
        columns = ColumnTypeIdentification.boolean_columns(df)
        result = df.copy()
        for column in columns:
            result[column] = (
                result[column]
                .map(lambda x: self._mapping.get(x, x) if pd.notna(x) else x)
                .astype("boolean")
            )

        return result

    def _get_report_data(self, before: pd.DataFrame, after: pd.DataFrame, report: ReportCollector):
        return ColumnTypeIdentification.boolean_columns(before)

    def _report(self, data, report: ReportCollector) -> str:
        if len(data) == 0:
            return "no columns converted"
        return f"convert these columns to boolean {', '.join(data)}"