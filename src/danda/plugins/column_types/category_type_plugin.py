import pandas as pd
from danda.plugins.column_types.type_plugin import TypePlugin
from danda.plugins.report_collector import ReportCollector


class CategoryTypePlugin(TypePlugin):
    """
    Convert low-cardinality columns to pandas category dtype.
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

            unique_count = df[column].nunique(dropna=True)
            unique_ratio = unique_count / n_rows

            if unique_ratio <= threshold:
                category_columns.append(column)

        return category_columns

    def _execute(self, df: pd.DataFrame, report: ReportCollector) -> pd.DataFrame:
        config = self._get_config_params(df)
        threshold = config.get("threshold")

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
        return self._find_category_columns(before)

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