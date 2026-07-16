from danda.plugins.plugin import Plugin
from danda.plugins.report_collector import ReportCollector


class TypePlugin(Plugin):
    def __init__(self, plugin_name: str, report: ReportCollector):
        super().__init__(plugin_name,"types", report)