from collections.abc import Sequence
import pandas as pd
from danda.plugins.plugin import Plugin

class ChainPlugin(Plugin):
    name: str = "ChainPlugin"
    def __init__(self, plugins: Sequence[Plugin]):
        self._plugins: list[Plugin] = []

        for plugin in plugins:
            self.add(plugin)

    def add(self, plugin: Plugin) -> None:
        if not isinstance(plugin, Plugin):
            raise TypeError(f"{plugin!r} is not a Plugin")
        self._plugins.append(plugin)
        return

    def execute(self, df: pd.DataFrame) -> pd.DataFrame:
        for plugin in self._plugins:
            df = plugin.execute(df)

        return df