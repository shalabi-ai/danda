import pandas as pd
from danda.plugins.column_types.type_plugin import TypePlugin
from danda.plugins.report_collector import ReportCollector

class NumericTypePlugin(TypePlugin):
    """
    Converts string columns containing numeric values to a pandas numeric data type (`int64` or `float64`, depending on the data). A column is converted when the fraction of successfully parsed non-missing values is greater than or equal to the configured threshold. Values that cannot be parsed are converted to `NaN`.

    Plugin Configuration:
    - numeric_enabled
    - numeric_threshold

    Example:

    input:
    pd.DataFrame({
        "Age": ["25", "30", "35", None],
        "Salary": ["50000.5", "62000", "71000.25", "80000"],
        "Name": ["Alice", "Bob", "Charlie", "David"]
    })

    Assume the configuration is:
    - numeric_threshold = 1.0

    output:
    pd.DataFrame({
        "Age": [25.0, 30.0, 35.0, pd.NA],
        "Salary": [50000.5, 62000.0, 71000.25, 80000.0],
        "Name": ["Alice", "Bob", "Charlie", "David"]
    })

    report:
    {
        "types": {
            "NumericTypePlugin": [
                "Age",
                "Salary"
            ]
        }
    }
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

