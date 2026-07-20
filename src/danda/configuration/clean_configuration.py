from danda.configuration.config_section import ConfigSection
from dataclasses import dataclass, field
from enum import Enum

class ColumnCase(str, Enum):
    SNAKE = "snake_case"
    CAMEL = "camelCase"
    LOWER = "lower"

@dataclass
class CleaningConfig(ConfigSection):
    remove_duplicates: bool = field(
        default=True,
        metadata={
            "description": "Remove duplicate rows from the DataFrame.",
            "feature": "Drop Duplicates"
        },
    )
    remove_duplicates_ignore_index: bool = field(
        default=False,
        metadata={
            "feature": "Drop Duplicates",
            "description": (
                "If True, reset the index after removing duplicate rows. "
                "Equivalent to the 'ignore_index' parameter of "
                "pandas.DataFrame.drop_duplicates()."
            ),
        },
    )

    strip_whitespace: bool = field(
        default=True,
        metadata={
            "description": "Remove leading and trailing whitespace from string values.",
            "feature": "Trim Whitespace"
        },
    )

    remove_empty_rows: bool = field(
        default=True,
        metadata={
            "description": "Remove rows where every value is missing.",
            "feature": "Remove Empty Rows"
        },
    )

    remove_empty_columns: bool = field(
        default=True,
        metadata={
            "description": "Remove columns where every value is missing.",
            "feature": "Remove Empty Columns"
        },
    )

    sparse_rows_enabled: bool = field(
        default=False,
        metadata={
            "description": (
                "Remove rows with too many missing values."
            ),
            "feature": "Sparse Rows",
        },
    )

    sparse_rows_threshold: float = field(
        default=0.8,
        metadata={
            "description": (
                "Maximum fraction of missing values allowed in a row. "
                "Rows with a higher fraction are removed."
            ),
            "feature": "Sparse Rows",
        },
    )

    sparse_columns_enabled: bool = field(
        default=False,
        metadata={
            "description": (
                "Remove columns with too many missing values."
            ),
            "feature": "Sparse Columns",
        },
    )

    sparse_columns_threshold: float = field(
        default=0.8,
        metadata={
            "description": (
                "Maximum fraction of missing values allowed in a column. "
                "Columns with a higher fraction are removed."
            ),
            "feature": "Sparse Columns",
        },
    )

    ## Rename column plugin
    rename_column_enabled: bool = field(
        default=False,
        metadata={
            "description": "Automatically rename DataFrame columns.",
            "feature": "Column Renaming",
        },
    )

    rename_column_style: ColumnCase = field(
        default=ColumnCase.SNAKE,
        metadata={
            "description": "Naming convention applied to column names.",
            "feature": "Column Renaming",
        },
    )
