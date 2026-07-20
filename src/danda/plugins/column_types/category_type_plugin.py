import pandas as pd
from danda.plugins.column_types.type_plugin import TypePlugin
from danda.plugins.report_collector import ReportCollector


class CategoryTypePlugin(TypePlugin):
    """
    Converts low-cardinality, non-numeric columns to the pandas `category` data type. A column is considered categorical when the ratio of unique non-missing values to the total number of rows is less than or equal to the configured threshold. Columns that are already boolean, datetime, categorical, or fully numeric are excluded.

    Plugin Configuration:
    - category_enabled
    - category_threshold

    Example:

    input:
    pd.DataFrame({
        "Color": ["Red", "Blue", "Red", "Blue", "Red"],
        "Department": ["HR", "IT", "HR", "IT", "HR"],
        "Name": ["Alice", "Bob", "Charlie", "David", "Eve"],
        "Age": [25, 30, 35, 40, 45]
    })

    Assume the configuration is:
    - category_threshold = 0.5

    output:
    pd.DataFrame({
        "Color": ["Red", "Blue", "Red", "Blue", "Red"],
        "Department": ["HR", "IT", "HR", "IT", "HR"],
        "Name": ["Alice", "Bob", "Charlie", "David", "Eve"],
        "Age": [25, 30, 35, 40, 45]
    }).astype({
        "Color": "category",
        "Department": "category"
    })

    report:
    {
        "types": {
            "CategoryTypePlugin": [
                "Color",
                "Department"
            ]
        }
    }
    """

    def __init__(self, report: ReportCollector):
        super().__init__("CategoryTypePlugin", report)

    @staticmethod
    def _find_category_columns(
            df: pd.DataFrame,
            threshold: float = 0.10,
    ) -> list[str]:
        """
        Return columns whose unique-value ratio is <= threshold.
        """
        category_columns = []

        n_rows = len(df)

        if n_rows == 0:
            return category_columns

        for column in df.columns:
            if (
                    pd.api.types.is_bool_dtype(df[column])
                    or pd.api.types.is_datetime64_any_dtype(df[column])
                    or pd.api.types.is_categorical_dtype(df[column])
            ):
                continue

            converted = pd.to_numeric(df[column].dropna(), errors="coerce")
            if converted.notna().mean() >= 1.0:
                # This is really a numeric column.
                continue

            unique_count = df[column].nunique(dropna=True)
            unique_ratio = unique_count / n_rows

            if unique_ratio <= threshold:
                category_columns.append(column)

        return category_columns

    def _execute(self, df: pd.DataFrame, report: ReportCollector) -> pd.DataFrame:
        config = self._get_config_params(df)
        threshold = config.get("threshold", .10)

        result = df.copy()

        columns = self._find_category_columns(df, threshold)

        for column in columns:
            result[column] = result[column].astype("category")

        return result

    def _get_report_data(
            self,
            before: pd.DataFrame,
            after: pd.DataFrame,
            report: ReportCollector,
    ):
        config = self._get_config_params(before)
        threshold = config.get("threshold", .10)
        return self._find_category_columns(before, threshold)

    def _report(self, data, report: ReportCollector) -> str:
        if not data:
            return "No category columns detected."

        return (
                "Converted the following columns to category: "
                + ", ".join(data)
        )

    def _get_config_params(self, df: pd.DataFrame) -> dict:
        config = self._get_config(df).types
        return {
            "enabled": config.category_enabled,
            "threshold": config.category_threshold
        }