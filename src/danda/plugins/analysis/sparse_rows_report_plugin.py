import pandas as pd

from danda.plugins.analysis.analysis_plugin import AnalysisPlugin
from danda.plugins.report_collector import ReportCollector


class SparseRowsReportPlugin(AnalysisPlugin):

    def __init__(self, report: ReportCollector):
        super().__init__("SparseRowsReportPlugin", report)

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
    ):
        config = self._get_config_params(before)

        threshold = config["threshold"]
        max_rows = config["max_rows"]

        total_columns = len(before.columns)

        if total_columns == 0:
            return []

        missing = before.isna().sum(axis=1)
        percent = missing / total_columns

        sparse = (
            pd.DataFrame({
                "missing": missing,
                "percent": percent,
            })
            .loc[percent >= threshold]
            .sort_values(
                by=["percent", "missing"],
                ascending=False,
            )
        )

        result = []

        for index, row in sparse.head(max_rows).iterrows():
            result.append({
                "index": index,
                "missing": int(row["missing"]),
                "total": total_columns,
                "percent": round(row["percent"] * 100, 1),
            })

        return result

    def _report(self, data, report: ReportCollector) -> str:
        if not data:
            return "No sparse rows detected."

        lines = ["Rows with many missing values:"]

        for row in data:
            lines.append(
                f"- Row {row['index']}: "
                f"{row['missing']}/{row['total']} missing "
                f"({row['percent']:.1f}%)"
            )

        omitted = (
            len(report.data["analysis"][self.report_name]) - len(data)
            if False else 0
        )

        if omitted:
            lines.append(f"... {omitted} more rows omitted.")

        return "\n".join(lines)

    def _get_config_params(self, df: pd.DataFrame) -> dict:
        config = self._get_config(df).analysis

        return {
            "enabled": config.sparse_rows_report_enabled,
            "threshold": config.sparse_rows_report_threshold,
            "max_rows": config.sparse_rows_report_max_rows,
        }
