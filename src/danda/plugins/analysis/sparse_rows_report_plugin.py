import pandas as pd

from danda.plugins.analysis.analysis_plugin import AnalysisPlugin
from danda.plugins.report_collector import ReportCollector


class SparseRowsReportPlugin(AnalysisPlugin):
    """
    Identifies rows containing a high proportion of missing values without modifying the DataFrame. A row is reported when the fraction of missing values is greater than or equal to the configured threshold. The report includes the row index, the number of missing values, the total number of columns, and the percentage of missing values. Results are sorted by missing percentage (highest first) and limited to the configured maximum number of rows.

    Plugin Configuration:
    - sparse_rows_report_enabled
    - sparse_rows_report_threshold
    - sparse_rows_report_max_rows

    Example:

    input:
    pd.DataFrame({
        "A": [1, None, None, 4],
        "B": [2, None, None, None],
        "C": [3, None, 5, None],
        "D": [4, None, None, 8]
    })

    Assume the configuration is:
    - sparse_rows_report_threshold = 0.75
    - sparse_rows_report_max_rows = 10

    output:
    pd.DataFrame({
        "A": [1, None, None, 4],
        "B": [2, None, None, None],
        "C": [3, None, 5, None],
        "D": [4, None, None, 8]
    })

    report:
    {
        "analysis": {
            "SparseRowsReportPlugin": [
                {
                    "index": 1,
                    "missing": 4,
                    "total": 4,
                    "percent": 100.0
                },
                {
                    "index": 2,
                    "missing": 3,
                    "total": 4,
                    "percent": 75.0
                },
                {
                    "index": 3,
                    "missing": 2,
                    "total": 4,
                    "percent": 50.0
                }
            ]
        }
    }
    """

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
