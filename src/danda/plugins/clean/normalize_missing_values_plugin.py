from danda.plugins.clean.clean_plugin import CleanPlugin
from danda.plugins.report_collector import ReportCollector
import pandas as pd


class NormalizeMissingValuesPlugin(CleanPlugin):
    """
    Normalizes user-defined representations of missing values by replacing matching string values with `pd.NA`. The plugin operates only on string columns and supports optional whitespace trimming and case-insensitive matching before comparing values. Existing missing values are preserved.

    Plugin Configuration:
    - normalize_enabled
    - normalize_values
    - normalize_strip_whitespace
    - normalize_ignore_case

    Example:

    input:
    pd.DataFrame({
        "Name": ["Alice", "N/A", "Bob", " unknown "],
        "City": ["New York", "None", "London", "Paris"],
        "Age": [25, 30, 35, 40]
    })

    Assume the configuration is:
    - normalize_values = ["N/A", "None", "Unknown"]
    - normalize_strip_whitespace = True
    - normalize_ignore_case = True

    output:
    pd.DataFrame({
        "Name": ["Alice", pd.NA, "Bob", pd.NA],
        "City": ["New York", pd.NA, "London", "Paris"],
        "Age": [25, 30, 35, 40]
    })

    report:
    {
        "missing": {
            "NormalizeMissingValuesPlugin": {
                "Name": 2,
                "City": 1
            }
        }
    }
    """
    def __init__(self, report: ReportCollector) -> None:
        super().__init__("NormalizeMissingValuesPlugin", report)

    def _execute(self, df: pd.DataFrame, report: ReportCollector) -> pd.DataFrame:
        config = self._get_config_params(df)

        values = set(config["values"])

        if config["ignore_case"]:
            values = {value.lower() for value in values}

        result = df.copy()

        object_columns = result.select_dtypes(
            include=["object", "string"]
        ).columns

        for column in object_columns:
            result[column] = result[column].map(
                lambda value: self._normalize_value(
                    value=value,
                    values=values,
                    strip_whitespace=config["strip_whitespace"],
                    ignore_case=config["ignore_case"],
                )
            )

        return result

    @staticmethod
    def _normalize_value(
            value,
            values: set[str],
            strip_whitespace: bool,
            ignore_case: bool,
    ):
        if not isinstance(value, str):
            return value

        candidate = value

        if strip_whitespace:
            candidate = candidate.strip()

        if ignore_case:
            candidate = candidate.lower()

        if candidate in values:
            return pd.NA

        return value

    def _get_report_data(
            self,
            before: pd.DataFrame,
            after: pd.DataFrame,
            report: ReportCollector,
    ) -> dict[str, int]:
        normalized = {}

        for column in before.columns:
            before_missing = before[column].isna().sum()
            after_missing = after[column].isna().sum()

            count = after_missing - before_missing

            if count:
                normalized[column] = count

        return normalized

    def _report(self, data: dict[str, int], report: ReportCollector) -> str:
        if not data:
            return "No missing values were normalized."

        total = sum(data.values())

        return (
            f"Normalized {total} missing value(s) "
            f"across {len(data)} column(s)."
        )

    def _get_config_params(self, df: pd.DataFrame) -> dict:
        config = self._get_config(df).missing

        return {
            "enabled": config.normalize_enabled,
            "values": config.normalize_values,
            "strip_whitespace": config.normalize_strip_whitespace,
            "ignore_case": config.normalize_ignore_case,
        }