from danda.plugins.clean.clean_plugin import CleanPlugin
from danda.plugins.report_collector import ReportCollector
import pandas as pd


class SparseRowsPlugin(CleanPlugin):

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