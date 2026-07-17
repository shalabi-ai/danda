import pandas as pd

from danda.plugins.column_types.column_type_identification import ColumnTypeIdentification
from danda.plugins.column_types.type_plugin import TypePlugin
from danda.plugins.report_collector import ReportCollector
from pandas.api.types import (
    is_string_dtype,
    is_object_dtype
)


class BooleanTypePlugin(TypePlugin):
    _mapping = {
        True: True,
        False: False,

        "1": True,
        "0": False,
        "true": True,
        "false": False,
        "True": True,
        "False": False,
    }
    _mapping_number = {
        1: True,
        0: False,
    }

    def __init__(self, report: ReportCollector):
        super().__init__("BooleanTypePlugin", report)

    def _execute(self, df: pd.DataFrame, report: ReportCollector) -> pd.DataFrame:
        mapping = {
            **self._mapping,
            **self._mapping_number,
        }
        columns = ColumnTypeIdentification.boolean_columns(df)
        result = df.copy()
        for column in columns:
            if is_string_dtype(result[column]) or is_object_dtype(result[column]):
                result[column] = result[column].str.lower()

            result[column] = (
                result[column]
                .replace(mapping) #.map(lambda x: self._mapping.get(x, x) if pd.notna(x) else x)
                .astype("boolean")
            )


        return result

    def _get_report_data(self, before: pd.DataFrame, after: pd.DataFrame, report: ReportCollector):
        return ColumnTypeIdentification.boolean_columns(before)

    def _report(self, data, report: ReportCollector) -> str:
        if len(data) == 0:
            return "no columns converted"
        return f"convert these columns to boolean {', '.join(data)}"

    def _get_config_params(self, df: pd.DataFrame) -> dict:
        config = self._get_config(df).types
        return {
            "enabled": config.boolean_enabled,
            #"threshold": config.boolean_threshold
        }