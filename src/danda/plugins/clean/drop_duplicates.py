import pandas as pd
from danda.plugins.clean.clean_plugin import CleanPlugin
from danda.plugins.report_collector import ReportCollector

class DropDuplicatesPlugin(CleanPlugin):
    """
    Removes duplicate rows from a pandas DataFrame using `pandas.DataFrame.drop_duplicates()`. The plugin preserves the first occurrence of each duplicated row and removes all subsequent duplicates. Optionally, the output DataFrame index can be reset based on the plugin configuration.

    Plugin Configuration:
    - remove_duplicates
    - remove_duplicates_ignore_index

    Example:

    input:
    pd.DataFrame({
        "A": [1, 2, 2, 3],
        "B": ["a", "b", "b", "c"],
    })

    output:
    pd.DataFrame({
        "A": [1, 2, 3],
        "B": ["a", "b", "c"],
    }, index=[0, 1, 3])

    report:
    {
        "clean": {
            "DropDuplicates": 1
        }
    }
    """
    def __init__(self, report: ReportCollector):
        super().__init__("DropDuplicates", report)

    def _execute(self, df: pd.DataFrame, report: ReportCollector) -> pd.DataFrame:
        config = self._get_config_params(df)
        ignore_index=config.get("ignore_index", False)
        return df.drop_duplicates(ignore_index=ignore_index)

    def _report(self, data, report: ReportCollector) -> str:
        return f"Number of deleted rows: {data}"

    def _get_report_data(self, before: pd.DataFrame, after: pd.DataFrame, report: ReportCollector):
        return len(before) - len(after)

    def _get_config_params(self, df: pd.DataFrame) -> dict:
        config = self._get_config(df).cleaning
        return {
            "enabled": config.remove_duplicates,
            "ignore_index": config.remove_duplicates_ignore_index
        }
