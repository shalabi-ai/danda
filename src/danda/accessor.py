import pandas as pd

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
        return

    def optimize(self):
        return

    def report(self):
        return