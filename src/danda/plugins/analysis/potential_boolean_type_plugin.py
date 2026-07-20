import pandas as pd
from danda.plugins.analysis.analysis_plugin import AnalysisPlugin
from danda.plugins.report_collector import ReportCollector
from pandas.api.types import (
    is_object_dtype,
    is_string_dtype,
)

class PotentialBooleanTypePlugin(AnalysisPlugin):
    """
    Identifies columns that may represent boolean values but are not in a recognized boolean format. A column is reported when it contains exactly two distinct non-missing values and those values are not already one of the supported boolean representations (`True`, `False`, `0`, `1`, `"true"`, `"false"`, `"0"`, or `"1"`). The plugin performs analysis only and does not modify the input DataFrame.

    Plugin Configuration:
    - potential_boolean_enabled

    Example:

    input:
    pd.DataFrame({
        "Subscribed": ["Yes", "No", "Yes", "No"],
        "Approved": ["Y", "N", "Y", "N"],
        "IsActive": ["true", "false", "true", "false"],
        "Status": ["Open", "Closed", "Pending", "Open"]
    })

    output:
    pd.DataFrame({
        "Subscribed": ["Yes", "No", "Yes", "No"],
        "Approved": ["Y", "N", "Y", "N"],
        "IsActive": ["true", "false", "true", "false"],
        "Status": ["Open", "Closed", "Pending", "Open"]
    })

    report:
    {
        "analysis": {
            "PotentialBooleanTypePlugin": {
                "Subscribed": ["Yes", "No"],
                "Approved": ["Y", "N"]
            }
        }
    }
    """
    def __init__(self, report: ReportCollector) -> None:
        super().__init__("PotentialBooleanTypePlugin", report)

    @staticmethod
    def _find_potential_boolean_columns(df: pd.DataFrame):
        boolean_values = {"true", "false", "0", "1"}

        candidates = {}

        for column in df.columns:
            series = df[column].dropna()

            if is_string_dtype(series) or is_object_dtype(series):
                values = series.astype(str).str.strip().str.lower().unique()
            else:
                values = series.unique()

            # Exactly two distinct values
            if len(values) != 2:
                continue

            normalized = {str(v).strip().lower() for v in values}

            # Skip columns that are already boolean-like
            if normalized.issubset(boolean_values):
                continue

            candidates[column] = list(values)

        return candidates

    def _execute(self, df: pd.DataFrame, report: ReportCollector) -> pd.DataFrame:
        # This plugin only reports; it doesn't modify the DataFrame.
        return df

    def _get_report_data(
            self,
            before: pd.DataFrame,
            after: pd.DataFrame,
            report: ReportCollector,
    ):
        return self._find_potential_boolean_columns(before)

    def _report(self, data, report: ReportCollector) -> str:
        if not data:
            return "No potential boolean columns found."

        lines = ["Columns that may represent boolean values:"]

        for column, values in data.items():
            lines.append(f" - {column}: {values}")

        return "\n".join(lines)

    def _get_config_params(self, df: pd.DataFrame) -> dict:
        config = self._get_config(df).types
        return {
            "enabled": config.potential_boolean_enabled,
        }