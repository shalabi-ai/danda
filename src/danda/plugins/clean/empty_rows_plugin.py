import pandas as pd
from danda.plugins.clean.clean_plugin import CleanPlugin
from danda.plugins.report_collector import ReportCollector


class EmptyRowsPlugin(CleanPlugin):
    """
    Removes rows that contain only missing values (NaN, pd.NA, etc.) from a pandas DataFrame. A row is removed only if every value in that row is missing. Rows containing at least one non-null value are preserved.

    Plugin Configuration:
    - remove_empty_rows

    Example:

    input:
    pd.DataFrame({
        "A": [1, None, 2, None],
        "B": ["x", None, "y", None]
    })

    output:
    pd.DataFrame({
        "A": [1, 2],
        "B": ["x", "y"]
    }, index=[0, 2])

    report:
    {
        "clean": {
            "EmptyRowsPlugin": 2
        }
    }
    """
    def __init__(self, report: ReportCollector):
        super().__init__("EmptyRowsPlugin", report)

    def _execute(self, df: pd.DataFrame, report: ReportCollector) -> pd.DataFrame:
        return df.dropna(how="all")

    def _report(self, data, report: ReportCollector) -> str:
        if data == 0:
            return "No empty rows deleted."
        return f"Number of deleted rows: {data}"

    def _get_report_data(self, before: pd.DataFrame, after: pd.DataFrame, report: ReportCollector):
        return before.index.size - after.index.size

    def _get_config_params(self, df: pd.DataFrame) -> dict:
        config = self._get_config(df).cleaning
        return {
            "enabled": config.remove_empty_rows
        }