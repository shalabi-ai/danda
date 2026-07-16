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
            "unknown",
            "?",
            "-",
            "--",
            "missing",
            "tbd",
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