from danda.plugins.plugin import Plugin
from danda.plugins.report_collector import ReportCollector


class CleanPlugin(Plugin):
    def __init__(self, plugin_name: str, report: ReportCollector) -> None:
        super().__init__(plugin_name, "clean", report)