import pandas as pd
from danda.plugins.chain import ChainPlugin
from danda.plugins.clean.drop_duplicates import DropDuplicatesPlugin
from danda.plugins.clean.empty_columns_plugin import EmptyColumnsPlugin
from danda.plugins.clean.empty_rows_plugin import EmptyRowsPlugin
from danda.plugins.clean.empty_spaces import EmptySpacesPlugin
from danda.plugins.column_types.boolean_type_plugin import BooleanTypePlugin
from danda.plugins.column_types.category_type_plugin import CategoryTypePlugin
from danda.plugins.column_types.datetime_type_plugin import DateTimeTypePlugin
from danda.plugins.column_types.numeric_type_plugin import NumericTypePlugin
from danda.plugins.optimization.information import DataFrameInformation
from danda.plugins.report_collector import ReportCollector


#
#df.dg.clean()
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