import pandas as pd

from danda.plugins.plugin import Plugin


class CounterPlugin(Plugin):
    name: str = "CounterPlugin"

    def __init__(self):
        self._counter = 0

    def execute(self, df: pd.DataFrame) -> pd.DataFrame:
        self._counter += 1
        return df

    def get_count(self)->int:
        return self._counter