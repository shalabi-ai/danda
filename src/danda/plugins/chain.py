from collections.abc import Sequence
import pandas as pd
from danda.plugins.optimization.information import DataFrameInformation
from danda.plugins.plugin import Plugin
from danda.plugins.report_collector import ReportCollector


class ChainPlugin(Plugin):
    """
    Executes a sequence of plugins in the order they were added, passing the output of each plugin as the input to the next. If a plugin raises an exception, the error is recorded in the report and execution continues with the remaining plugins. After execution, the plugin reports the number of plugins executed, their names, and the change in DataFrame memory usage.

    Plugin Configuration:
    - None (always enabled)

    Example:

    Assume the chain contains the following plugins:
    1. EmptyRowsPlugin
    2. DropDuplicates
    3. RenameColumnsPlugin

    input:
    pd.DataFrame({
        "First Name": ["Alice", "Bob", "Bob", None],
        "Age": [25, 30, 30, None]
    })

    output:
    pd.DataFrame({
        "first_name": ["Alice", "Bob"],
        "age": [25.0, 30.0]
    }, index=[0, 1])

    report:
    {
        "chain": {
            "ChainPlugin": {
                "plugins_count": 3,
                "plugin_names": [
                    "EmptyRowsPlugin",
                    "DropDuplicates",
                    "RenameColumnsPlugin"
                ],
                "memory_usage": {
                    "before": 396,
                    "after": 270,
                    "difference": -126,
                    "percent": -31.8
                }
            }
        }
    }
    """
    def __init__(self, plugins: Sequence[Plugin], report: ReportCollector):
        super().__init__("ChainPlugin", "chain", report)

        self._plugins: list[Plugin] = []

        for plugin in plugins:
            self.add(plugin)

    def add(self, plugin: Plugin) -> None:
        if not isinstance(plugin, Plugin):
            raise TypeError(f"{plugin!r} is not a Plugin")
        self._plugins.append(plugin)
        return

    def _execute(self, df: pd.DataFrame, report: ReportCollector) -> pd.DataFrame:
        current_plugin: Plugin

        for plugin in self._plugins:
            try:
                current_plugin = plugin
                df = plugin.run(df, report)
            except Exception as exc:
                report.add_report("exception", current_plugin.plugin_name, str(exc))

        return df

    def _report(self, data, report: ReportCollector):
        return {
            "plugins_count": data["plugins_count"],
            "plugin_names": data["plugin_names"],
            "memory_usage": data["memory_usage"],
           # "result": deepcopy(self.chain_collector.report),
        }

    def _get_report_data(self, before: pd.DataFrame, after: pd.DataFrame, report: ReportCollector):
        return {
            "plugins_count": len(self._plugins),
            "plugin_names": [p.plugin_name for p in self._plugins],
            "memory_usage": DataFrameInformation.evaluate_memory_usage(before, after)
            #"result": deepcopy(self.chain_collector.data),
        }

    def _get_config_params(self, df: pd.DataFrame) -> dict:
        return {
            "enabled" : True
        }