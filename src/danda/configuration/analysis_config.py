from dataclasses import dataclass, field
from danda.configuration.config_section import ConfigSection

@dataclass
class AnalysisConfig(ConfigSection):
    empty_value_enabled: bool = field(
        default=True,
        metadata={
            "description": (
                "Detect values that may represent missing data but "
                "are not automatically converted."
            ),
            "feature": "Potential Missing Value Detection",
        },
    )

    empty_value_values: tuple[str, ...] = field(
        default=(
            "n/a",
            "na",
            "?",
            "-",
            "--",
        ),
        metadata={
            "description": (
                "Text values to report as potential missing values."
            ),
            "feature": "Potential Missing Value Detection",
        },
    )

    empty_value_strip_whitespace: bool = field(
        default=True,
        metadata={
            "description": (
                "Strip leading and trailing whitespace from string values "
                "before checking whether they represent missing values."
            ),
            "feature": "Potential Missing Value Detection",
        },
    )

    empty_value_ignore_case: bool = field(
        default=True,
        metadata={
            "description": (
                "Compare candidate missing values without considering "
                "letter casing."
            ),
            "feature": "Potential Missing Value Detection",
        },
    )

    suspicious_missing_enabled: bool = field(
        default=True,
        metadata={
            "description": (
                "Detect values that are commonly used as "
                "sentinel values for missing data."
            ),
            "feature": "Suspicious Missing Values",
        },
    )

    suspicious_missing_values: tuple = field(
        default=(
            -9999,
            -999,
            999,
            9999,
            99999,
            2147483647,
            -1,
            "UNKNOWN",
            "MISSING",
            "TBD",
            "TBA",
            "PENDING",
        ),
        metadata={
            "description": (
                "Values to report as suspicious missing values."
            ),
            "feature": "Suspicious Missing Values",
        },
    )

    suspicious_missing_ignore_case: bool = field(
        default=True,
        metadata={
            "description": (
                "Compare string sentinel values without considering case."
            ),
            "feature": "Suspicious Missing Values",
        },
    )

    suspicious_missing_strip_whitespace: bool = field(
        default=True,
        metadata={
            "description": (
                "Strip leading and trailing whitespace from string values "
                "before checking whether they match suspicious missing values."
            ),
            "feature": "Suspicious Missing Values",
        },
    )