from danda.configuration.config_section import ConfigSection
from dataclasses import dataclass, field

@dataclass
class TypeConfig(ConfigSection):

    boolean_enabled: bool = field(
        default=True,
        metadata={
            "description": (
                "Enable automatic detection and conversion of boolean columns."
            ),
            "feature": "Boolean Detection",
        },
    )

    boolean_threshold: float = field(
        default=1.0,
        metadata={
            "description": (
                "Minimum fraction of non-null values that must be "
                "boolean-like (True/False, 0/1, Yes/No, etc.) before "
                "the column is considered boolean."
            ),
            "feature": "Boolean Detection",
        },
    )

    datetime_enabled: bool = field(
        default=True,
        metadata={
            "description": (
                "Enable automatic detection and conversion of datetime columns."
            ),
            "feature": "Datetime Detection",
        },
    )

    datetime_threshold: float = field(
        default=0.95,
        metadata={
            "description": (
                "Minimum fraction of non-null values that must be "
                "successfully converted to datetime before the column "
                "is considered a datetime column."
            ),
            "feature": "Datetime Detection",
        },
    )

    numeric_enabled: bool = field(
        default=True,
        metadata={
            "description": (
                "Enable automatic detection and conversion of numeric columns."
            ),
            "feature": "Numeric Detection",
        },
    )

    numeric_threshold: float = field(
        default=0.95,
        metadata={
            "description": (
                "Minimum fraction of non-null values that must be "
                "successfully converted to numeric before the column "
                "is considered numeric."
            ),
            "feature": "Numeric Detection",
        },
    )

    category_enabled: bool = field(
        default=True,
        metadata={
            "description": (
                "Enable automatic detection and conversion of categorical columns."
            ),
            "feature": "Category Detection",
        },
    )

    category_threshold: float = field(
        default=0.10,
        metadata={
            "description": (
                "Maximum ratio of unique non-null values for a column "
                "to be converted to the pandas 'category' dtype."
            ),
            "feature": "Category Detection",
        },
    )