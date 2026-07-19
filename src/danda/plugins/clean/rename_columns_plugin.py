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
    """
    Renames DataFrame columns according to the configured naming convention. Supported naming styles are `snake_case`, `camelCase`, and `lowercase`. If multiple columns would result in the same name after conversion, the plugin automatically appends a numeric suffix (for example, `_2`, `_3`) to ensure all column names remain unique.

    Plugin Configuration:
    - rename_column_enabled
    - rename_column_style

    Example:

    input:
    pd.DataFrame({
        "First Name": ["Alice", "Bob"],
        "Last-Name": ["Smith", "Jones"],
        "Employee.ID": [101, 102],
        "First_Name": ["A", "B"]
    })

    Assume the configuration is:
    - rename_column_style = ColumnCase.SNAKE

    output:
    pd.DataFrame({
        "first_name": ["Alice", "Bob"],
        "last_name": ["Smith", "Jones"],
        "employee_id": [101, 102],
        "first_name_2": ["A", "B"]
    })

    report:
    {
        "clean": {
            "RenameColumnsPlugin": {
                "renamed": [
                    "employee_id",
                    "first_name",
                    "first_name_2",
                    "last_name"
                ],
                "count": 4
            }
        }
    }
    """

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

        }
        columns: set[str] = set()
        for col in result.columns:
            new = func(col)
            if new in columns:
                new = self._unique_column_name(new, columns)
            columns.add(new)
            mapping[col] = func(new)

        result = result.rename(columns=mapping)

        return result

    def _unique_column_name(self, name: str, names: set[str]) -> str:
        old = name
        count = 2

        while name in names:
            name = f"{old}_{count}"
            count += 1

        return name
    def _get_report_data(self, before, after, report):
        columns: set[str] = set()

        for old, new in zip(before.columns, after.columns):
            if old != new:
                if new in columns:
                    new = self._unique_column_name(new, columns)
                columns.add(new)

        list_columns = list(columns)
        list_columns.sort()

        return {
            "renamed": list_columns,
            "count": len(columns),
        }

    def _report(self, data, report):
        if data["count"] == 0:
            return "No columns were renamed."

        columns = ", ".join(data["renamed"])
        return f"Renamed {data['count']} column(s). columns: {columns}"

    def _get_config_params(self, df):
        config = self._get_config(df)

        return {
            "enabled": config.cleaning.rename_column_enabled,
            "style": config.cleaning.rename_column_style,
        }
