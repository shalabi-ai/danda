from danda.plugins.clean.clean_plugin import CleanPlugin
from danda.plugins.report_collector import ReportCollector
import pandas as pd


class SparseColumnsPlugin(CleanPlugin):

    def __init__(self, report: ReportCollector) -> None:
        super().__init__(
            plugin_name="SparseColumnsPlugin",
            report=report,
        )

    def _execute(
            self,
            df: pd.DataFrame,
            report: ReportCollector,
    ) -> pd.DataFrame:
        threshold = self._get_config_params(df)["threshold"]

        missing_fraction = df.isna().mean(axis=0)

        columns_to_keep = missing_fraction < threshold

        return df.loc[:, columns_to_keep].copy()

    def _get_report_data(
            self,
            before: pd.DataFrame,
            after: pd.DataFrame,
            report: ReportCollector,
    ):
        removed = before.columns.difference(after.columns)

        return {
            "columns_removed": len(removed),
            "columns": removed.tolist(),
        }

    def _report(self, data, report: ReportCollector) -> str:
        if data["columns_removed"] == 0:
            return "No sparse columns removed."

        return (
                f"Removed {data['columns_removed']} sparse "
                f"column{'s' if data['columns_removed'] != 1 else ''}: "
                + ", ".join(data["columns"])
        )

    def _get_config_params(self, df: pd.DataFrame) -> dict:
        config = self._get_config(df).cleaning

        return {
            "enabled": config.sparse_columns_enabled,
            "threshold": config.sparse_columns_threshold,
        }