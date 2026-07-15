import pandas as pd

class ColumnTypeIdentification:

    @staticmethod
    def boolean_columns(df: pd.DataFrame) -> list[str]:
        """
        Return columns whose non-null values are all boolean-like.

        Accepted values:
        - True, False
        - 0, 1
        - "True", "False"
        - "true", "false"
        - "0", "1"
        """

        valid_values = {"true", "false", "0", "1"}

        boolean_cols = []

        for col in df.columns:
            values = {
                str(v).strip().lower()
                for v in df[col].dropna().unique()
            }

            if values and values.issubset(valid_values):
                boolean_cols.append(col)

        return boolean_cols

