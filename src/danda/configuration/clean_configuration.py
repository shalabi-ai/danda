from danda.configuration.config_section import ConfigSection
from dataclasses import dataclass, field


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