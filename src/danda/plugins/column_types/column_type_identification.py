import pandas as pd

class ColumnTypeIdentification:
    """
    Identifies DataFrame columns whose non-missing values can be interpreted as boolean values. A column is classified as boolean if every non-null value is one of the supported boolean representations: `True`, `False`, `0`, `1`, `"true"`, `"false"`, `"0"`, or `"1"`. String comparisons are performed after trimming leading/trailing whitespace and converting values to lowercase.

    This utility is used by type conversion plugins to automatically detect columns that can be safely converted to the pandas nullable `boolean` data type.

    Example:

    input:
    pd.DataFrame({
        "IsActive": ["True", "false", "1", "0", None],
        "Verified": [1, 0, 1, None, 0],
        "Status": ["Yes", "No", "Yes", "No", None],
        "Age": [25, 30, 35, 40, 45]
    })

    output:
    ["IsActive", "Verified"]
    """

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

