import pandas as pd


class DataFrameInformation:

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def information(self)->pd.DataFrame:
        info_data = pd.DataFrame(index=df.columns)
        info_data["Types"] = df.dtypes #types["type"]
        info_data["NonNullCounts"] = df.count().values
        info_data["MemoryUsage"] = df.memory_usage(index=False)
        info_data["UniqueCounts"] = df.nunique()

        return info_data.reset_index(names="Columns")

    @staticmethod
    def get_string_columns(df: pd.DataFrame) -> list[str]:
        string_columns = df.select_dtypes(include=["object", "string"]).columns

        return string_columns