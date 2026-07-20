from danda.plugins.analysis.analysis_plugin import AnalysisPlugin
from danda.plugins.report_collector import ReportCollector

import pandas as pd


class ConstantColumnsPlugin(AnalysisPlugin):
    """
    Identifies columns whose non-missing values are all identical. A column is considered constant if it contains exactly one unique non-null value, regardless of the number of missing values. The plugin performs analysis only and does not modify the input DataFrame.

    Plugin Configuration:
    - None (always enabled)

    Example:

    input:
    pd.DataFrame({
        "Country": ["USA", "USA", "USA", None],
        "Status": ["Active", "Inactive", "Active", "Inactive"],
        "Version": [1, 1, 1, 1],
        "Score": [10, 20, 30, 40]
    })

    output:
    pd.DataFrame({
        "Country": ["USA", "USA", "USA", None],
        "Status": ["Active", "Inactive", "Active", "Inactive"],
        "Version": [1, 1, 1, 1],
        "Score": [10, 20, 30, 40]
    })

    report:
    {
        "analysis": {
            "ConstantColumns": {
                "Country": "USA",
                "Version": 1
            }
        }
    }
    """

    def __init__(self, report: ReportCollector):
        super().__init__("ConstantColumns", report)

    def _execute(self, df: pd.DataFrame, report: ReportCollector) -> pd.DataFrame:
        return df

    def _get_report_data(
        self,
        before: pd.DataFrame,
        after: pd.DataFrame,
        report: ReportCollector,
    ) -> dict[str, object]:

        result = {}

        for column in before.columns:
            values = before[column].dropna().unique()

            if len(values) == 1:
                result[column] = values[0]

        return result

    def _report(self, data, report: ReportCollector) -> str:
        if not data:
            return "No constant columns detected."

        lines = ["Constant columns detected:"]

        for column, value in data.items():
            lines.append(f"- {column}: {value!r}")

        return "\n".join(lines)

    def _get_config_params(self, df: pd.DataFrame) -> dict:
        return {"enabled": True}
