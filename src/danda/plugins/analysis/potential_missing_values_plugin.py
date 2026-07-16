from collections import Counter
import pandas as pd
from danda.plugins.analysis.analysis_plugin import AnalysisPlugin
from danda.plugins.report_collector import ReportCollector


class PotentialMissingValuesPlugin(AnalysisPlugin):

    def __init__(self, report: ReportCollector) -> None:
        super().__init__("PotentialMissingValuesPlugin", report)

    def _execute(self, df: pd.DataFrame, report: ReportCollector) -> pd.DataFrame:
        # Analysis plugins never modify the dataframe.
        return df

    def _get_report_data(
            self,
            before: pd.DataFrame,
            after: pd.DataFrame,
            report: ReportCollector,
    ) -> dict[str, dict[str, int]]:
        config = self._get_config_params(before)

        values = set(config["values"])

        if config["ignore_case"]:
            values = {v.lower() for v in values}

        result = {}

        object_columns = before.select_dtypes(
            include=["object", "string"]
        ).columns

        for column in object_columns:
            counter = Counter()

            for value in before[column].dropna():

                if not isinstance(value, str):
                    continue

                candidate = value

                if config["strip_whitespace"]:
                    candidate = candidate.strip()

                if config["ignore_case"]:
                    candidate = candidate.lower()

                if candidate in values:
                    counter[value] += 1

            if counter:
                result[column] = dict(counter)

        return result

    def _report(self, data, report: ReportCollector) -> str:
        if not data:
            return "No potential missing values detected."

        lines = ["Potential missing values detected:"]

        for column, values in data.items():
            summary = ", ".join(
                f"{value} ({count})"
                for value, count in values.items()
            )
            lines.append(f"- {column}: {summary}")

        return "\n".join(lines)

    def _get_config_params(self, df: pd.DataFrame) -> dict:
        config = self._get_config(df).analysis

        return {
            "enabled": config.empty_value_enabled,
            "values": config.empty_value_values,
            "strip_whitespace": config.empty_value_strip_whitespace,
            "ignore_case": config.empty_value_ignore_case,
        }