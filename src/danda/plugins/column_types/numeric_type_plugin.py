import pandas as pd
from danda.plugins.column_types.type_plugin import TypePlugin
from danda.plugins.report_collector import ReportCollector

class NumericTypePlugin(TypePlugin):
    """
    Convert string columns containing numeric values to numeric dtype.
    """

    def __init__(self, report: ReportCollector) -> None:
        super().__init__("NumericTypePlugin", report)

    @staticmethod
    def _find_numeric_columns(
            df: pd.DataFrame,
            success_threshold: float = 1.0,
    ) -> list[str]:
        """
        Find object/string columns that can be converted to numeric.
        """
        numeric_columns = []

        for column in df.columns:
            if not (
                    pd.api.types.is_object_dtype(df[column])
                    or pd.api.types.is_string_dtype(df[column])
            ):
                continue

            non_null = df[column].dropna()

            if non_null.empty:
                continue

            converted = pd.to_numeric(non_null, errors="coerce")

            success_rate = converted.notna().mean()

            if success_rate >= success_threshold:
                numeric_columns.append(column)

        return numeric_columns

    def _execute(self, df: pd.DataFrame, report: ReportCollector) -> pd.DataFrame:
        config = self._get_config_params(df)
        threshold = config.get("threshold")

        result = df.copy()

        columns = self._find_numeric_columns(df, threshold)

        for column in columns:
            result[column] = pd.to_numeric(result[column], errors="coerce")

        return result

    def _get_report_data(
            self,
            before: pd.DataFrame,
            after: pd.DataFrame,
            report: ReportCollector,
    ):
        return self._find_numeric_columns(before)

    def _report(self, data, report: ReportCollector) -> str:
        if not data:
            return "No numeric columns detected."

        return (
                "Converted the following columns to numeric: "
                + ", ".join(data)
        )

    def _get_config_params(self, df: pd.DataFrame) -> dict:
        config = self._get_config(df).types
        return {
            "enabled": config.numeric_enabled,
            "threshold": config.numeric_threshold
        }

