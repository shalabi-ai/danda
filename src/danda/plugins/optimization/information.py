import pandas as pd


class DataFrameInformation:

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def information(self)->pd.DataFrame:
        info_data = pd.DataFrame(index=self.df.columns)
        info_data["Types"] = self.df.dtypes #types["type"]
        info_data["NonNullCounts"] = self.df.count().values
        info_data["MemoryUsage"] = self.df.memory_usage(index=False)
        info_data["UniqueCounts"] = self.df.nunique()

        return info_data.reset_index(names="Columns")

    @staticmethod
    def get_string_columns(df: pd.DataFrame) -> list[str]:
        string_columns = df.select_dtypes(include=["object", "string"]).columns

        return string_columns

    import pandas as pd

    @staticmethod
    def evaluate_memory_usage(before: pd.DataFrame, after: pd.DataFrame) -> dict:
        """
        Compare memory usage between two DataFrames.

        Returns
        -------
        dict
            {
                "before_bytes": int,
                "after_bytes": int,
                "saved_bytes": int,
                "saved_percent": float,
            }
        """

        before_total = before.memory_usage(deep=True).sum()
        after_total = after.memory_usage(deep=True).sum()

        saved_bytes = before_total - after_total

        return {
            "before_bytes": before_total,
            "after_bytes": after_total,
            "saved_bytes": saved_bytes,
            "saved_percent": (
                saved_bytes / before_total * 100
                if before_total
                else 0.0
            ),
        }