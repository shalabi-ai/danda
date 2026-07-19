import pandas as pd

from danda.configuration.clean_configuration import ColumnCase
from danda.plugins.clean.clean_plugin import CleanPlugin
from danda.plugins.report_collector import ReportCollector
import re


def snake_case(name: str) -> str:
    name = str(name).strip()

    # camelCase -> camel_Case
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)

    # separators
    name = re.sub(r"[\s\-./]+", "_", name)

    # collapse
    name = re.sub(r"_+", "_", name)

    return name.lower().strip("_")


def camel_case(name: str) -> str:
    words = snake_case(name).split("_")

    if not words:
        return ""

    return words[0] + "".join(w.title() for w in words[1:])


def lower_case(name: str) -> str:
    return str(name).strip().lower()


class RenameColumnsPlugin(CleanPlugin):

    def __init__(self, report: ReportCollector):
        super().__init__(
            plugin_name="RenameColumnsPlugin",
            report=report,
        )

    def _execute(self, df: pd.DataFrame, report: ReportCollector) -> pd.DataFrame:
        result = df.copy()

        config = self._get_config_params(df)

        style = config["style"]

        if style == ColumnCase.SNAKE:
            func = snake_case
        elif style == ColumnCase.CAMEL:
            func = camel_case
        elif style == ColumnCase.LOWER:
            func = lower_case
        else:
            return result

        mapping = {
            col: func(col)
            for col in result.columns
        }

        result = result.rename(columns=mapping)

        return result

    def _get_report_data(self, before, after, report):
        renamed = {
            old: new
            for old, new in zip(before.columns, after.columns)
            if old != new
        }

        return {
            "renamed": renamed,
            "count": len(renamed),
        }

    def _report(self, data, report):
        if data["count"] == 0:
            return "No columns were renamed."

        columns = ", ".join(data["renamed"].values())
        return f"Renamed {data['count']} column(s). columns: {columns}"

    def _get_config_params(self, df):
        config = self._get_config(df)

        return {
            "enabled": config.cleaning.rename_column_enabled,
            "style": config.cleaning.rename_column_style,
        }
