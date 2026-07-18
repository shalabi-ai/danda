from danda.plugins.analysis.analysis_plugin import AnalysisPlugin
from danda.plugins.report_collector import ReportCollector

import pandas as pd


class ColumnSummaryPlugin(AnalysisPlugin):

    def __init__(self, report: ReportCollector):
        super().__init__("ColumnSummary", report)

    def _execute(self, df: pd.DataFrame, report: ReportCollector) -> pd.DataFrame:
        return df

    def _get_report_data(
        self,
        before: pd.DataFrame,
        after: pd.DataFrame,
        report: ReportCollector,
    ) -> dict[str, dict]:

        result = {}
        rows = len(before)

        for column in before.columns:
            missing = before[column].isna().sum()
            result[column] = {
                "dtype": str(before[column].dtype),
                "missing": int(before[column].isna().sum()),
                "missing_percent": int(missing * 100 / rows),
                "unique": int(before[column].nunique(dropna=True)),
            }

        return result

    def _report(self, data, report: ReportCollector) -> str:
        lines = ["Column Summary:"]

        for column, stats in data.items():
            lines.extend(
                [
                    "",
                    column,
                    f"Type: {stats['dtype']}",
                    f"Missing: {stats['missing']} ({stats['missing_percent']}%)",
                    f"Unique: {stats['unique']}",
                ]
            )

        return "\n".join(lines)

    def _get_config_params(self, df: pd.DataFrame) -> dict:
        return {"enabled": True}