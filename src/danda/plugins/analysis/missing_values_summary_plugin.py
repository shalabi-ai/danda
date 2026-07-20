from danda.plugins.analysis.analysis_plugin import AnalysisPlugin
from danda.plugins.report_collector import ReportCollector
import pandas as pd


class MissingValuesSummaryPlugin(AnalysisPlugin):
    """
    Provides an overall summary of missing values in the DataFrame without modifying the data. The summary includes the total number of rows and columns, the number and percentage of missing cells, the number of columns containing missing values, the number of rows containing missing values, and the number and percentage of complete rows.

    Plugin Configuration:
    - None (always enabled)

    Example:

    input:
    pd.DataFrame({
        "Name": ["Alice", None, "Charlie", "David"],
        "Age": [25, None, 35, 40],
        "City": ["London", "Paris", None, None]
    })

    output:
    pd.DataFrame({
        "Name": ["Alice", None, "Charlie", "David"],
        "Age": [25, None, 35, 40],
        "City": ["London", "Paris", None, None]
    })

    report:
    {
        "analysis": {
            "MissingValuesSummaryPlugin": {
                "rows": 4,
                "columns": 3,
                "missing_cells": 4,
                "missing_percent": 33.3,
                "columns_with_missing": 3,
                "rows_with_missing": 3,
                "complete_rows": 1,
                "complete_rows_percent": 25.0
            }
        }
    }
    """

    def __init__(self, report: ReportCollector):
        super().__init__("MissingValuesSummaryPlugin", report)

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
        rows = len(before)
        columns = len(before.columns)

        total_cells = rows * columns

        missing_cells = int(before.isna().sum().sum())

        missing_percent = (
            missing_cells / total_cells * 100
            if total_cells
            else 0.0
        )

        columns_with_missing = int(before.isna().any().sum())

        rows_with_missing = int(before.isna().any(axis=1).sum())

        complete_rows = rows - rows_with_missing

        complete_rows_percent = (
            complete_rows / rows * 100
            if rows
            else 0.0
        )

        return {
            "rows": rows,
            "columns": columns,
            "missing_cells": missing_cells,
            "missing_percent": round(missing_percent, 1),
            "columns_with_missing": columns_with_missing,
            "rows_with_missing": rows_with_missing,
            "complete_rows": complete_rows,
            "complete_rows_percent": round(
                complete_rows_percent,
                1,
            ),
        }

    def _report(self, data, report: ReportCollector):

        return (
            "Missing Value Summary\n"
            f"Rows: {data['rows']}\n"
            f"Columns: {data['columns']}\n\n"
            f"Missing cells: {data['missing_cells']} "
            f"({data['missing_percent']:.1f}%)\n"
            f"Columns with missing: {data['columns_with_missing']}\n"
            f"Rows with missing: {data['rows_with_missing']}\n"
            f"Complete rows: {data['complete_rows']} "
            f"({data['complete_rows_percent']:.1f}%)"
        )

    def _get_config_params(self, df: pd.DataFrame) -> dict:
        return {
            "enabled": True,
        }