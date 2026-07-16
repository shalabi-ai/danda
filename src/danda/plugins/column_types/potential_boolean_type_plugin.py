import pandas as pd
from danda.plugins.column_types.type_plugin import TypePlugin
from danda.plugins.report_collector import ReportCollector


class PotentialBooleanTypePlugin(TypePlugin):
    def __init__(self, report: ReportCollector) -> None:
        super().__init__("PotentialBooleanTypePlugin", report)

    @staticmethod
    def _find_potential_boolean_columns(df: pd.DataFrame):
        boolean_values = {"true", "false", "0", "1"}

        candidates = {}

        for column in df.columns:
            values = df[column].dropna().unique()

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

        lines = ["Potential boolean columns detected:"]

        for column, values in data.items():
            lines.append(f" - {column}: {values}")

        return "\n".join(lines)

    def _get_config_params(self, df: pd.DataFrame) -> dict:
        config = self._get_config(df).types
        return {
            "enabled": config.potential_boolean_enabled,
        }