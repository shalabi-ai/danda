import pandas as pd
from danda.plugins.column_types.type_plugin import TypePlugin
from danda.plugins.report_collector import ReportCollector


class DateTimeTypePlugin(TypePlugin):
    """
    Convert string columns that appear to contain datetimes into
    pandas datetime64 dtype.
    """

    def __init__(self, report: ReportCollector):
        super().__init__("DateTimeTypePlugin", report)

    @staticmethod
    def _find_datetime_columns(
            df: pd.DataFrame,
            success_threshold: float = 0.9,
    ) -> list[str]:
        """
        Find object/string columns that can be parsed as datetimes.

        Parameters
        ----------
        success_threshold : float
            Fraction of non-null values that must successfully parse.
        """
        datetime_columns = []

        for column in df.columns:
            if not (
                    pd.api.types.is_object_dtype(df[column])
                    or pd.api.types.is_string_dtype(df[column])
            ):
                continue

            non_null = df[column].dropna()

            if non_null.empty:
                continue

            parsed = pd.to_datetime(non_null, errors="coerce", format="mixed",)

            success_rate = parsed.notna().mean()

            if success_rate >= success_threshold:
                datetime_columns.append(column)

        return datetime_columns

    def _execute(self, df: pd.DataFrame, report: ReportCollector) -> pd.DataFrame:
        config = self._get_config_params(df)
        threshold = config.get("threshold")

        result = df.copy()

        columns = self._find_datetime_columns(df, threshold)

        for column in columns:
            result[column] = pd.to_datetime(result[column], errors="coerce", format="mixed",)

        return result

    def _get_report_data(
            self,
            before: pd.DataFrame,
            after: pd.DataFrame,
            report: ReportCollector,
    ):
        return self._find_datetime_columns(before)

    def _report(self, data, report: ReportCollector) -> str:
        if not data:
            return "No datetime columns detected."

        return (
                "Converted the following columns to datetime: "
                + ", ".join(data)
        )

    def _get_config_params(self, df: pd.DataFrame) -> dict:
        config = self._get_config(df).types
        return {
            "enabled": config.datetime_enabled,
            "threshold": config.datetime_threshold
        }