from abc import ABC, abstractmethod
import pandas as pd


class Plugin(ABC):
    name: str = "plugin"

    @abstractmethod
    def execute(self, df: pd.DataFrame) -> pd.DataFrame:
        pass
