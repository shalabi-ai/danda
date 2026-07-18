import pandas as pd
from danda.configuration.danda_configuration import DandaConfig
from danda.plugins.analysis.column_summary_plugin import ColumnSummaryPlugin
from danda.plugins.analysis.constant_columns_plugin import ConstantColumnsPlugin
from danda.plugins.analysis.missing_values_report_plugin import MissingValuesReportPlugin
from danda.plugins.analysis.missing_values_summary_plugin import MissingValuesSummaryPlugin
from danda.plugins.analysis.potential_missing_values_plugin import PotentialMissingValuesPlugin
from danda.plugins.analysis.sparse_rows_report_plugin import SparseRowsReportPlugin
from danda.plugins.analysis.suspicious_missing_values_plugin import SuspiciousMissingValuesPlugin
from danda.plugins.chain import ChainPlugin
from danda.plugins.clean.drop_duplicates import DropDuplicatesPlugin
from danda.plugins.clean.empty_columns_plugin import EmptyColumnsPlugin
from danda.plugins.clean.empty_rows_plugin import EmptyRowsPlugin
from danda.plugins.clean.empty_spaces import EmptySpacesPlugin
from danda.plugins.clean.normalize_missing_values_plugin import NormalizeMissingValuesPlugin
from danda.plugins.clean.sparse_columns_plugin import SparseColumnsPlugin
from danda.plugins.clean.sparse_rows_plugin import SparseRowsPlugin
from danda.plugins.column_types.boolean_type_plugin import BooleanTypePlugin
from danda.plugins.column_types.category_type_plugin import CategoryTypePlugin
from danda.plugins.column_types.datetime_type_plugin import DateTimeTypePlugin
from danda.plugins.column_types.numeric_type_plugin import NumericTypePlugin
from danda.plugins.analysis.potential_boolean_type_plugin import PotentialBooleanTypePlugin
from danda.plugins.imputation.impute_missing_values_plugin import ImputeMissingValuesPlugin
from danda.plugins.optimization.information import DataFrameInformation
from danda.plugins.report_collector import ReportCollector


def clean(df: pd.DataFrame) -> pd.DataFrame:
    return df.dg.clean()
#
#df.dg.optimize()
#
#df.dg.report()

@pd.api.extensions.register_dataframe_accessor("dg")
class DandaAccessor:

    def __init__(self, pandas_obj):
        self._df = pandas_obj

    def clean(self):
        report_collector = ReportCollector()
        plugins = [
            EmptySpacesPlugin(report_collector),
            NormalizeMissingValuesPlugin(report_collector),
            SparseColumnsPlugin(report_collector),
            SparseRowsPlugin(report_collector),
            EmptyRowsPlugin(report_collector),
            EmptyColumnsPlugin(report_collector),
            DropDuplicatesPlugin(report_collector),
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

    def analyze(self):
        report_collector = ReportCollector()
        plugins = [
            ColumnSummaryPlugin(report_collector),
            MissingValuesSummaryPlugin(report_collector),
            MissingValuesReportPlugin(report_collector),
            PotentialMissingValuesPlugin(report_collector),
            SuspiciousMissingValuesPlugin(report_collector),
            SparseRowsReportPlugin(report_collector),
            PotentialBooleanTypePlugin(report_collector),
            ConstantColumnsPlugin(report_collector),
            #PotentialDateTimeTypePlugin(report_collector),
            #PotentialCategoryTypePlugin(report_collector),
            #PotentialMissingValuesPlugin(report_collector),
            #MixedTypesPlugin(report_collector),
            #ConstantColumnsPlugin(report_collector),
        ]

        chain_plugin = ChainPlugin(plugins, report_collector)
        result = chain_plugin.run(self._df)

        # Preserve existing attrs
        result.attrs.update(self._df.attrs)
        result.attrs["danda_analyze_report"] = report_collector.report

        return result

    def impute(self):
        report_collector = ReportCollector()
        plugins = [
            ImputeMissingValuesPlugin(report_collector)
        ]

        chain_plugin = ChainPlugin(plugins, report_collector)
        result = chain_plugin.run(self._df)

        # Preserve existing attrs
        result.attrs.update(self._df.attrs)
        result.attrs["danda_impute_report"] = report_collector.report

        return result

    @property
    def report(self):
        reports = {}

        if "danda_clean_report" in self._df.attrs:
            reports["clean"] = self._df.attrs["danda_clean_report"]

        if "danda_optimize_report" in self._df.attrs:
            reports["optimize"] = self._df.attrs["danda_optimize_report"]

        if "danda_analyze_report" in self._df.attrs:
            reports["analyze"] = self._df.attrs["danda_analyze_report"]

        if "danda_impute_report" in self._df.attrs:
            reports["impute"] = self._df.attrs["danda_impute_report"]

        return reports

    def compare_memory(self, other: pd.DataFrame) -> dict:
        return DataFrameInformation.evaluate_memory_usage(self._df, other)

    @property
    def config(self) -> DandaConfig:
        if "danda_config" not in self._df.attrs:
            self._df.attrs["danda_config"] = DandaConfig()

        return self._df.attrs["danda_config"]
