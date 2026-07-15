from abc import ABC, abstractmethod
import pandas as pd
from typing import Any

from danda.plugins.report_collector import ReportCollector


class Plugin(ABC):
    def __init__(self, plugin_name: str, plugin_category: str, report: ReportCollector):
        self.plugin_name = plugin_name
        self.plugin_category = plugin_category
        self.report_name = plugin_name
        self.report_collector = report


    def run(self, df: pd.DataFrame, report: ReportCollector | None = None,) -> pd.DataFrame:
        if report is None:
            report = self.report_collector

        self.report_name = self._unique_plugin_name(report)

        result = self._execute(df, report)

        data = self._get_report_data(df, result, report)

        report.add_report(self.plugin_category, self.report_name, self._report(data, report))
        report.add_data(self.plugin_category, self.report_name, data)

        return result

    def _unique_plugin_name(self, report: ReportCollector) -> str:
        name = self.plugin_name
        count = 2

        while report.exists(self.plugin_category, name):
            name = f"{self.plugin_name}_{count}"
            count += 1

        return name

    @abstractmethod
    def _execute(self, df: pd.DataFrame, report: ReportCollector) -> pd.DataFrame:
        pass

    @abstractmethod
    def _get_report_data(self, before: pd.DataFrame, after: pd.DataFrame, report: ReportCollector):
        pass

    @abstractmethod
    def _report(self, data, report: ReportCollector) -> str:
        pass