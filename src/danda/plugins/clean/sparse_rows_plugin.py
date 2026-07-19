from danda.plugins.clean.clean_plugin import CleanPlugin
from danda.plugins.report_collector import ReportCollector
import pandas as pd


class SparseRowsPlugin(CleanPlugin):
    """
    Removes rows whose fraction of missing values is greater than or equal to the configured threshold. The missing-value fraction is calculated independently for each row as the number of missing values divided by the total number of columns. Rows with a missing-value fraction below the threshold are retained.

    Plugin Configuration:
    - sparse_rows_enabled
    - sparse_rows_threshold

    Example:

    input:
    pd.DataFrame({
        "A": [1, None, None, 4],
        "B": [10, None, 30, None],
        "C": [100, None, None, 400],
        "D": [1000, None, 4000, None]
    })

    Assume the configuration is:
    - sparse_rows_threshold = 0.75

    output:
    pd.DataFrame({
        "A": [1, None, 4],
        "B": [10, 30, None],
        "C": [100, None, 400],
        "D": [1000, 4000, None]
    }, index=[0, 2, 3])

    report:
    {
        "clean": {
            "SparseRowsPlugin": {
                "rows_removed": 1,
                "indices": [1]
            }
        }
    }
    """

    def __init__(self, report: ReportCollector) -> None:
        super().__init__("SparseRowsPlugin", report)

    def _execute(self, df: pd.DataFrame, report: ReportCollector) -> pd.DataFrame:
        threshold = self._get_config_params(df)["threshold"]

        missing_fraction = df.isna().mean(axis=1)

        return df.loc[missing_fraction < threshold].copy()

    def _get_report_data(
            self,
            before: pd.DataFrame,
            after: pd.DataFrame,
            report: ReportCollector,
    ):
        removed = before.index.difference(after.index)

        return {
            "rows_removed": len(removed),
            "indices": removed.tolist(),
        }

    def _report(self, data, report: ReportCollector) -> str:
        if data["rows_removed"] == 0:
            return "No sparse rows removed."

        return (
            f"Removed {data['rows_removed']} sparse "
            f"row{'s' if data['rows_removed'] != 1 else ''}."
        )

    def _get_config_params(self, df: pd.DataFrame) -> dict:
        config = self._get_config(df).cleaning

        return {
            "enabled": config.sparse_rows_enabled,
            "threshold": config.sparse_rows_threshold,
        }