from dataclasses import dataclass, field
from danda.configuration.config_section import ConfigSection
from typing import Literal

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

    sparse_rows_report_enabled: bool = field(
        default=True,
        metadata={
            "description": (
                "Report rows containing a high proportion of missing values."
            ),
            "feature": "Sparse Row Reporting",
        },
    )

    sparse_rows_report_threshold: float = field(
        default=0.5,
        metadata={
            "description": (
                "Minimum proportion of missing values required for a row "
                "to be reported. Values must be between 0.0 and 1.0."
            ),
            "feature": "Sparse Row Reporting",
        },
    )

    sparse_rows_report_max_rows: int = field(
        default=20,
        metadata={
            "description": (
                "Maximum number of sparse rows to include in the report."
            ),
            "feature": "Sparse Row Reporting",
        },
    )

    ###################
    #outlier
    ################
    outlier_enabled: bool = field(
        default=True,
        metadata={
            "description": (
                "Enable detection of outliers in numeric columns."
            ),
            "feature": "Outlier Detection",
        },
    )

    outlier_method: Literal["iqr", "zscore"] = field(
        default="iqr",
        metadata={
            "description": (
                "Statistical method used to identify outliers. "
                "'iqr' uses the interquartile range, while 'zscore' "
                "uses the standard score."
            ),
            "feature": "Outlier Detection",
        },
    )

    outlier_iqr_multiplier: float = field(
        default=1.5,
        metadata={
            "description": (
                "Multiplier applied to the interquartile range (IQR) "
                "when calculating the lower and upper bounds for "
                "outlier detection."
            ),
            "feature": "Outlier Detection",
        },
    )

    outlier_zscore_threshold: float = field(
        default=3.0,
        metadata={
            "description": (
                "Absolute Z-score threshold above which a value is "
                "considered an outlier."
            ),
            "feature": "Outlier Detection",
        },
    )

    outlier_max_examples: int = field(
        default=10,
        metadata={
            "description": (
                "Maximum number of outlier examples to include in "
                "analysis reports for each column."
            ),
            "feature": "Outlier Detection",
        },
    )

    outlier_include_examples: bool = field(
        default=True,
        metadata={
            "description": (
                "Include example row indices and values for detected "
                "outliers in the analysis report."
            ),
            "feature": "Outlier Detection",
        },
    )

    outlier_note_threshold: float = field(
        default=5.0,
        metadata={
            "description": (
                "Minimum percentage of detected outliers required before "
                "displaying a note that the distribution may be naturally "
                "skewed rather than indicative of data quality issues."
            ),
            "feature": "Outlier Detection",
        },
    )