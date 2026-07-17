from danda.plugins.analysis.analysis_plugin import AnalysisPlugin
from danda.plugins.report_collector import ReportCollector
import pandas as pd


class MissingValuesReportPlugin(AnalysisPlugin):

    def __init__(self, report: ReportCollector) -> None:
        super().__init__("MissingValuesReportPlugin", report)

    def _execute(self, df: pd.DataFrame, report: ReportCollector) -> pd.DataFrame:
        return df

    def _get_report_data(self, before: pd.DataFrame, after: pd.DataFrame, report: ReportCollector) -> dict[str, dict[str, float]]:

        total_rows = len(before)

        result = {}

        for column in before.columns:
            missing = before[column].isna().sum()

            if missing == 0:
                continue

            result[column] = {
                "count": int(missing),
                "percent": round(
                    missing / total_rows * 100,
                    1,
                    ),
            }

        return result

    def _report(self, data, report: ReportCollector) -> str:
        if not data:
            return "No missing values detected."

        sorted_items = sorted(
            data.items(),
            key=lambda item: (
                -item[1]["percent"],
                -item[1]["count"],
                item[0],
            ),
        )

        lines = ["Missing values detected:"]

        for column, stats in sorted_items:
            lines.append(
                f"- {column}: {stats['count']} ({stats['percent']}%)"
            )

        return "\n".join(lines)

    def _get_config_params(self, df: pd.DataFrame) -> dict:
        return {"enabled": True}