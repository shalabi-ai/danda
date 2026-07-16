danda is a DataFrame preparation library.

Its job is to take a DataFrame that has just been loaded and make it ready for analysis with safe, deterministic transformations.

The philosophy

danda should perform operations that are:

Objective (there is little ambiguity)
Safe (low risk of changing the meaning of the data)
Automatic (users almost always want them)

For example:


Remove completely empty rows
Remove completely empty columns
Trim whitespace
Normalize common null values
Convert "1" → 1
Convert "True" → True
Convert "2024-01-01" → datetime
Convert low-cardinality strings → category
Reduce int64 → int8
Generate reports

These improve the DataFrame without making assumptions about the underlying data.

The solution provides a dataframe accessor.
```python
@pd.api.extensions.register_dataframe_accessor("dg")
class DandaAccessor:

    def __init__(self, pandas_obj):
        self._df = pandas_obj

    def clean(self):
        report_collector = ReportCollector()
        plugins = [
            EmptyRowsPlugin(report_collector),
            EmptyColumnsPlugin(report_collector),
            DropDuplicatesPlugin(report_collector),
            EmptySpacesPlugin(report_collector),
        ]
        chain_plugin = ChainPlugin(plugins, report_collector)
        result = chain_plugin.run(self._df)

        # Preserve existing attrs
        result.attrs.update(self._df.attrs)
        result.attrs["danda_clean_report"] = report_collector.report

        return result

    def optimize(self):
        report_collector = ReportCollector()
        plugins = [
            BooleanTypePlugin(report_collector),
            DateTimeTypePlugin(report_collector),
            NumericTypePlugin(report_collector),
            CategoryTypePlugin(report_collector),
        ]

        chain_plugin = ChainPlugin(plugins, report_collector)
        result = chain_plugin.run(self._df)

        # Preserve existing attrs
        result.attrs.update(self._df.attrs)
        result.attrs["danda_optimize_report"] = report_collector.report

        return result


    @property
    def report(self):
        reports = {}

        if "danda_clean_report" in self._df.attrs:
            reports["clean"] = self._df.attrs["danda_clean_report"]

        if "danda_optimize_report" in self._df.attrs:
            reports["optimize"] = self._df.attrs["danda_optimize_report"]

        return reports

    def compare_memory(self, other: pd.DataFrame) -> dict:
        return DataFrameInformation.evaluate_memory_usage(self._df, other)

    @property
    def config(self) -> DandaConfig:
        if "danda_config" not in self._df.attrs:
            self._df.attrs["danda_config"] = DandaConfig()

        return self._df.attrs["danda_config"]
```

Ths solution is a plugin architecture, this is our plugin:
```python
class Plugin(ABC):
    def __init__(self, plugin_name: str, plugin_category: str, report: ReportCollector):
        self.plugin_name = plugin_name
        self.plugin_category = plugin_category
        self.report_name = plugin_name
        self.report_collector = report


    @final
    def run(self, df: pd.DataFrame, report: ReportCollector | None = None,) -> pd.DataFrame:
        params = self._get_config_params(df)
        if not params.get("enabled", True):
            return df

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
    def _report(self, data, report: ReportCollector):
        pass

    @abstractmethod
    def _get_config_params(self, df: pd.DataFrame) -> dict:
        pass

    def _get_config(self, df: pd.DataFrame) -> DandaConfig:
        return df.dg.config
```

The solution provide configuration for example:
```python
@dataclass
class TypeConfig(ConfigSection):
    datetime_enabled: bool = field(
        default=True,
        metadata={
            "description": (
                "Enable automatic detection and conversion of datetime columns."
            ),
            "feature": "Datetime Detection",
        },
    )

    datetime_threshold: float = field(
        default=1.0,
        metadata={
            "description": (
                "Minimum fraction of non-null values that must be "
                "successfully converted to datetime before the column "
                "is considered a datetime column."
            ),
            "feature": "Datetime Detection",
        },
    )
```
