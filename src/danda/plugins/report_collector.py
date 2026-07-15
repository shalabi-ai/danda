from typing import Any


class ReportCollector:
    def __init__(self):
        self._report_data: dict[str, dict[str, Any]] = {}
        self._report: dict[str, dict[str, str]] = {}

    def add_data(self, category: str, name: str, data: Any) -> None:
        self._report_data.setdefault(category, {})
        self._report_data[category][name] = data

    def add_report(self, category: str, name: str, report: str) -> None:
        self._report.setdefault(category, {})
        self._report[category][name] = report

    @property
    def data(self) -> dict[str, dict[str, Any]]:
        return self._report_data

    @property
    def report(self) -> dict[str, dict[str, str]]:
        return self._report

    def exists(self, category: str, name: str) -> bool:
        return name in self._report_data.get(category, {})