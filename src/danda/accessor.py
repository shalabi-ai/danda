import pandas as pd
from danda.plugins import report_collector
from danda.plugins.chain import ChainPlugin
from danda.plugins.clean.drop_duplicates import DropDuplicatesPlugin
from danda.plugins.clean.empty_columns_plugin import EmptyColumnsPlugin
from danda.plugins.clean.empty_rows_plugin import EmptyRowsPlugin
from danda.plugins.clean.empty_spaces import EmptySpacesPlugin
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
        self.report_collector = ReportCollector()

    def clean(self):
        plugins = [
            EmptyRowsPlugin(self.report_collector),
            EmptyColumnsPlugin(self.report_collector),
            DropDuplicatesPlugin(self.report_collector),
            EmptySpacesPlugin(self.report_collector),
        ]
        chain_plugin = ChainPlugin(plugins, self.report_collector)
        result = chain_plugin.run(self._df)
        result.attrs["danda_report"] = self.report_collector.report

        return result

    def optimize(self):
        return

    @property
    def report(self):
        return self._df.attrs.get("danda_report")