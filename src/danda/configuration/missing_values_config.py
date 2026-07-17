from dataclasses import dataclass, field
from danda.configuration.config_section import ConfigSection

@dataclass
class MissingValuesConfig(ConfigSection):
    normalize_enabled: bool = field(
        default=True,
        metadata={
            "description": (
                "Enable normalization of common textual representations "
                "of missing values to pandas missing values (pd.NA)."
            ),
            "feature": "Missing Value Normalization",
        },
    )

    normalize_values: tuple[str, ...] = field(
        default=(
            "",
            "null",
            "none",
            "nan",
            "<na>",
        ),
        metadata={
            "description": (
                "Text values that should be treated as missing. "
                "Comparison is performed after applying the configured "
                "whitespace and case normalization options."
            ),
            "feature": "Missing Value Normalization",
        },
    )

    normalize_strip_whitespace: bool = field(
        default=True,
        metadata={
            "description": (
                "Strip leading and trailing whitespace from string values "
                "before checking whether they represent missing values."
            ),
            "feature": "Missing Value Normalization",
        },
    )

    normalize_ignore_case: bool = field(
        default=True,
        metadata={
            "description": (
                "Compare candidate missing values without considering "
                "letter casing."
            ),
            "feature": "Missing Value Normalization",
        },
    )