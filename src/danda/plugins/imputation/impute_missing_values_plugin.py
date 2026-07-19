import pandas as pd
from danda.plugins.imputation.impute_plugin import ImputePlugin
from danda.plugins.report_collector import ReportCollector
from pandas.api.types import (
    is_bool_dtype,
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_string_dtype,
)



class ImputeMissingValuesPlugin(ImputePlugin):
    """
    Imputes missing values according to the data type of each column and the configured imputation strategy. Different strategies can be configured independently for numeric, boolean, categorical, datetime, and text columns. The plugin fills only missing values and leaves all existing values unchanged.

    Supported strategies include:
    - **Numeric:** `mean`, `median`, `mode`, `constant`
    - **Boolean:** `mode`, `constant`
    - **Categorical:** `mode`, `constant`
    - **Datetime:** `ffill`, `bfill`, `constant`
    - **Text:** `mode`, `constant`, `empty`

    Plugin Configuration:
    - enabled
    - numeric_strategy
    - numeric_constant
    - boolean_strategy
    - boolean_constant
    - category_strategy
    - category_constant
    - datetime_strategy
    - datetime_constant
    - text_strategy
    - text_constant

    Example:

    input:
    pd.DataFrame({
        "Age": [25, None, 35, 40],
        "IsActive": pd.Series([True, None, True, False], dtype="boolean"),
        "Department": pd.Series(["HR", None, "IT", "HR"], dtype="category"),
        "JoinDate": pd.to_datetime(["2024-01-01", None, "2024-01-03", "2024-01-04"]),
        "City": ["London", None, "Paris", "London"]
    })

    Assume the configuration is:
    - numeric_strategy = "median"
    - boolean_strategy = "mode"
    - category_strategy = "mode"
    - datetime_strategy = "ffill"
    - text_strategy = "constant"
    - text_constant = "Unknown"

    output:
    pd.DataFrame({
        "Age": [25.0, 35.0, 35.0, 40.0],
        "IsActive": pd.Series([True, True, True, False], dtype="boolean"),
        "Department": pd.Series(["HR", "HR", "IT", "HR"], dtype="category"),
        "JoinDate": pd.to_datetime([
            "2024-01-01",
            "2024-01-01",
            "2024-01-03",
            "2024-01-04"
        ]),
        "City": ["London", "Unknown", "Paris", "London"]
    })

    report:
    {
        "imputation": {
            "ImputeMissingValuesPlugin": {
                "Age": {
                    "strategy": "median",
                    "filled": 1
                },
                "IsActive": {
                    "strategy": "mode",
                    "filled": 1
                },
                "Department": {
                    "strategy": "mode",
                    "filled": 1
                },
                "JoinDate": {
                    "strategy": "ffill",
                    "filled": 1
                },
                "City": {
                    "strategy": "constant",
                    "filled": 1
                }
            }
        }
    }
    """

    def __init__(self, report: ReportCollector):
        super().__init__(
            plugin_name="ImputeMissingValuesPlugin",
            report=report,
        )
        self._config: dict[str, object] = {}

    def _median_value(self, s: pd.Series):
        value = s.median()
        return None if pd.isna(value) else value

    def _mean_value(self, s: pd.Series):
        value = s.mean()
        return None if pd.isna(value) else value

    def _mode_value(self, s: pd.Series):
        mode = s.mode(dropna=True)
        return None if mode.empty else mode.iloc[0]

    def _execute(
            self,
            df: pd.DataFrame,
            report: ReportCollector,
    ) -> pd.DataFrame:
        self._config = self._get_config_params(df)
        result = df.copy()

        for column in result.columns:

            missing = result[column].isna().sum()

            if missing == 0:
                continue

            series = result[column]

            if is_bool_dtype(series):
                result[column] = self._fill_boolean(series)

            elif is_datetime64_any_dtype(series):
                result[column] = self._fill_datetime(series)

            elif is_categorical_dtype(series):
            #elif isinstance(series, pd.CategoricalDtype): did not work
                result[column] = self._fill_category(series)

            elif is_numeric_dtype(series):
                result[column] = self._fill_numeric(series)

            elif is_string_dtype(series) or series.dtype == object:
                result[column] = self._fill_text(series)

        return result

    def _fill_numeric(self, s: pd.Series) -> pd.Series:
        strategy = self.config["numeric_strategy"]

        if strategy == "median":
            value = self._median_value(s)
            if value is None:
                return s
            #value = s.median()
        elif strategy == "mean":
            value = self._mean_value(s)
            if value is None:
                return s
            #value = s.mean()
        elif strategy == "mode":
            value = self._mode_value(s)
            if value is None:
                return s
            #value = s.mode().iloc[0]
        elif strategy == "constant":
            value = self.config["numeric_constant"]
        else:
            return s

        return s.fillna(value)

    def _fill_boolean(self, s: pd.Series) -> pd.Series:
        strategy = self.config["boolean_strategy"]

        if strategy == "mode":
            value = self._mode_value(s)
            if value is None:
                return s
            #value = s.mode().iloc[0]
        elif strategy == "constant":
            value = self.config["boolean_constant"]
        else:
            return s

        return s.fillna(value)

    def _fill_category(self, s: pd.Series) -> pd.Series:
        strategy = self.config["category_strategy"]

        if strategy == "mode":
            value = self._mode_value(s)
            if value is None:
                return s
            #value = s.mode().iloc[0]

            if value not in s.cat.categories:
                s = s.cat.add_categories([value])

        elif strategy == "constant":
            value = self.config["category_constant"]

            if value not in s.cat.categories:
                s = s.cat.add_categories([value])

        else:
            return s

        return s.fillna(value)

    def _fill_datetime(self, s: pd.Series) -> pd.Series:
        strategy = self.config["datetime_strategy"]

        if strategy == "ffill":
            return s.ffill()

        if strategy == "bfill":
            return s.bfill()

        if strategy == "constant":
            return s.fillna(self.config["datetime_constant"])

        return s

    def _fill_text(self, s: pd.Series) -> pd.Series:
        strategy = self.config["text_strategy"]

        if strategy == "mode":
            value = self._mode_value(s)
            if value is None:
                return s
            #value = s.mode().iloc[0]

        elif strategy == "constant":
            value = self.config["text_constant"]

        elif strategy == "empty":
            value = ""

        else:
            return s

        return s.fillna(value)

    def _get_report_data(
            self,
            before: pd.DataFrame,
            after: pd.DataFrame,
            report: ReportCollector,
    ):
        result = {}

        for column in before.columns:
            count = before[column].isna().sum()

            if count == 0:
                continue

            if is_bool_dtype(before[column]):
                strategy = self.config["boolean_strategy"]
            elif is_datetime64_any_dtype(before[column]):
                strategy = self.config["datetime_strategy"]
            elif is_categorical_dtype(before[column]):
                strategy = self.config["category_strategy"]
            elif is_numeric_dtype(before[column]):
                strategy = self.config["numeric_strategy"]
            else:
                strategy = self.config["text_strategy"]

            result[column] = {
                "strategy": strategy,
                "filled": int(count),
            }

        return result

    def _report(self, data, report: ReportCollector):

        if not data:
            return "No missing values imputed."

        lines = ["Filled missing values:"]

        for column, info in data.items():
            lines.append(
                f"- {column}: {info['strategy']} ({info['filled']})"
            )

        return "\n".join(lines)

    def _get_config_params(self, df: pd.DataFrame) -> dict:
        config = self._get_config(df).imputation

        return {
            "enabled": config.enabled,
            "numeric_strategy": config.numeric_strategy,
            "numeric_constant": config.numeric_constant,

            "boolean_strategy": config.boolean_strategy,
            "boolean_constant": config.boolean_constant,

            "category_strategy": config.category_strategy,
            "category_constant": config.category_constant,

            "datetime_strategy": config.datetime_strategy,
            "datetime_constant": config.datetime_constant,

            "text_strategy": config.text_strategy,
            "text_constant": config.text_constant,
        }

    @property
    def config(self):
        return self._config