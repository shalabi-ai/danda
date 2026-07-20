from collections import Counter
import pandas as pd
from danda.plugins.analysis.analysis_plugin import AnalysisPlugin
from danda.plugins.report_collector import ReportCollector

class PotentialMissingValuesPlugin(AnalysisPlugin):
    """
    Identifies string values that are likely intended to represent missing data without modifying the DataFrame. The plugin searches string columns for user-configured placeholder values (such as `"N/A"`, `"Unknown"`, or `"None"`), with optional whitespace trimming and case-insensitive matching. The report lists each column containing potential missing values together with the number of occurrences of each configured placeholder.

    Plugin Configuration:
    - empty_value_enabled
    - empty_value_values
    - empty_value_strip_whitespace
    - empty_value_ignore_case

    Example:

    input:
    pd.DataFrame({
        "Name": ["Alice", "N/A", "Bob", " unknown "],
        "City": ["London", "None", "Paris", "Berlin"],
        "Department": ["HR", "IT", "Unknown", "HR"],
        "Age": [25, 30, 35, 40]
    })

    Assume the configuration is:
    - empty_value_values = ["N/A", "None", "Unknown"]
    - empty_value_strip_whitespace = True
    - empty_value_ignore_case = True

    output:
    pd.DataFrame({
        "Name": ["Alice", "N/A", "Bob", " unknown "],
        "City": ["London", "None", "Paris", "Berlin"],
        "Department": ["HR", "IT", "Unknown", "HR"],
        "Age": [25, 30, 35, 40]
    })

    report:
    {
        "analysis": {
            "PotentialMissingValuesPlugin": {
                "Name": {
                    "N/A": 1,
                    "Unknown": 1
                },
                "City": {
                    "None": 1
                },
                "Department": {
                    "Unknown": 1
                }
            }
        }
    }
    """

    def __init__(self, report: ReportCollector) -> None:
        super().__init__("PotentialMissingValuesPlugin", report)

    def _execute(
            self,
            df: pd.DataFrame,
            report: ReportCollector,
    ) -> pd.DataFrame:
        # Analysis plugins never modify the dataframe.
        return df

    def _get_report_data(
            self,
            before: pd.DataFrame,
            after: pd.DataFrame,
            report: ReportCollector,
    ) -> dict[str, dict[str, int]]:
        config = self._get_config_params(before)

        # Build lookup: normalized configured value -> canonical configured value
        lookup = {}

        for value in config["values"]:
            candidate = value

            if config["strip_whitespace"]:
                candidate = candidate.strip()

            if config["ignore_case"]:
                candidate = candidate.lower()

            lookup[candidate] = value

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

                if candidate in lookup:
                    counter[lookup[candidate]] += 1

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