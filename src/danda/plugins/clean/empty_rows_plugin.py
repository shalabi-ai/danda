import pandas as pd

from danda.plugins.plugin import Plugin


class EmptyRowsPlugin(Plugin):
    name: str = "EmptyRowsPlugin"

    def execute(self, df: pd.DataFrame) -> pd.DataFrame:
        return df