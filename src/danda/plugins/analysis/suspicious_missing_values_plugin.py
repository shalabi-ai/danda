from danda.plugins.analysis.analysis_plugin import AnalysisPlugin
from danda.plugins.report_collector import ReportCollector
import pandas as pd


class SuspiciousMissingValuesPlugin(AnalysisPlugin):
    """
    Identifies values that may indicate missing data without modifying the DataFrame. The plugin searches all columns for user-configured suspicious values, such as placeholders like `"?"`, `"-"`, `"Unknown"`, `"Missing"`, or other domain-specific indicators. Matching can optionally ignore letter casing and leading/trailing whitespace. The report lists each column containing suspicious values together with the number of occurrences of each detected indicator.

    Plugin Configuration:
    - suspicious_missing_enabled
    - suspicious_missing_values
    - suspicious_missing_ignore_case
    - suspicious_missing_strip_whitespace

    Example:

    input:
    pd.DataFrame({
        "Name": ["Alice", "Unknown", "Bob", " Missing "],
        "City": ["London", "?", "Paris", "-"],
        "Department": ["HR", "IT", "Unknown", "HR"],
        "Age": [25, 30, 35, 40]
    })

    Assume the configuration is:
    - suspicious_missing_values = ["Unknown", "Missing", "?", "-"]
    - suspicious_missing_ignore_case = True
    - suspicious_missing_strip_whitespace = True

    output:
    pd.DataFrame({
        "Name": ["Alice", "Unknown", "Bob", " Missing "],
        "City": ["London", "?", "Paris", "-"],
        "Department": ["HR", "IT", "Unknown", "HR"],
        "Age": [25, 30, 35, 40]
    })

    report:
    {
        "analysis": {
            "SuspiciousMissingValuesPlugin": {
                "Name": {
                    "Unknown": 1,
                    "Missing": 1
                },
                "City": {
                    "?": 1,
                    "-": 1
                },
                "Department": {
                    "Unknown": 1
                }
            }
        }
    }
    """

    def __init__(self, report: ReportCollector) -> None:
        super().__init__(
            plugin_name="SuspiciousMissingValuesPlugin",
            report=report,
        )

    def _execute(
            self,
            df: pd.DataFrame,
            report: ReportCollector,
    ) -> pd.DataFrame:
        return df

    def _get_report_data(
            self,
            before: pd.DataFrame,
            after: pd.DataFrame,
            report: ReportCollector,
    ):
        config = self._get_config_params(before)

        suspicious_values = config["values"]
        ignore_case = config["ignore_case"]
        strip_whitespace = config["strip_whitespace"]

        normalized_lookup = {}

        for value in suspicious_values:
            if isinstance(value, str):
                normalized = value

                if strip_whitespace:
                    normalized = normalized.strip()

                if ignore_case:
                    normalized = normalized.lower()

                normalized_lookup[normalized] = value
            else:
                normalized_lookup[value] = value

        result = {}

        for column in before.columns:
            counts = {}

            for value in before[column].dropna():
                candidate = value

                if isinstance(candidate, str):
                    if strip_whitespace:
                        candidate = candidate.strip()

                    if ignore_case:
                        candidate = candidate.lower()

                if candidate in normalized_lookup:
                    original = normalized_lookup[candidate]
                    counts[original] = counts.get(original, 0) + 1

            if counts:
                result[column] = counts

        return result

    def _report(self, data, report: ReportCollector) -> str:
        if not data:
            return "No suspicious missing values detected."

        lines = ["Suspicious missing value indicators detected:"]

        for column, values in data.items():
            formatted = ", ".join(
                f"{value} ({count})"
                for value, count in values.items()
            )

            lines.append(f"- {column}: {formatted}")

        return "\n".join(lines)

    def _get_config_params(self, df: pd.DataFrame) -> dict:
        config = self._get_config(df).analysis

        return {
            "enabled": config.suspicious_missing_enabled,
            "values": config.suspicious_missing_values,
            "ignore_case": config.suspicious_missing_ignore_case,
            "strip_whitespace": config.suspicious_missing_strip_whitespace,
        }
