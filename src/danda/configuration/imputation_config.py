from dataclasses import dataclass, field
from typing import Literal

from danda.configuration.config_section import ConfigSection


@dataclass
class ImputationConfig(ConfigSection):

    enabled: bool = field(
        default=False,
        metadata={
            "description": (
                "Enable automatic filling of missing values."
            ),
            "feature": "Missing Value Imputation",
        },
    )

    numeric_strategy: Literal[
        "median",
        "mean",
        "mode",
        "constant",
    ] = field(
        default="median",
        metadata={
            "description": (
                "Strategy used to fill missing values in numeric columns."
            ),
            "feature": "Numeric Imputation",
        },
    )

    numeric_constant: int | float = field(
        default=0,
        metadata={
            "description": (
                "Constant value used when the numeric strategy is "
                "'constant'."
            ),
            "feature": "Numeric Imputation",
        },
    )

    boolean_strategy: Literal[
        "mode",
        "constant",
    ] = field(
        default="mode",
        metadata={
            "description": (
                "Strategy used to fill missing values in boolean columns."
            ),
            "feature": "Boolean Imputation",
        },
    )

    boolean_constant: bool = field(
        default=False,
        metadata={
            "description": (
                "Constant value used when the boolean strategy is "
                "'constant'."
            ),
            "feature": "Boolean Imputation",
        },
    )

    category_constant: str = field(
        default="Unknown",
        metadata={
            "description": (
                "Constant value used when the categorical strategy is "
                "'constant'."
            ),
            "feature": "Categorical Imputation",
        },
    )

    category_strategy: Literal[
        "mode",
        "constant",
    ] = field(
        default="mode",
        metadata={
            "description": (
                "Strategy used to fill missing values in categorical columns."
            ),
            "feature": "Categorical Imputation",
        },
    )

    datetime_strategy: Literal[
        "ffill",
        "bfill",
        "constant",
    ] = field(
        default="ffill",
        metadata={
            "description": (
                "Strategy used to fill missing values in datetime columns."
            ),
            "feature": "Datetime Imputation",
        },
    )

    datetime_constant: str | None = field(
        default=None,
        metadata={
            "description": (
                "Constant datetime value used when the datetime strategy "
                "is 'constant'. The value should be parseable by pandas."
            ),
            "feature": "Datetime Imputation",
        },
    )

    text_constant: str = field(
        default="Unknown",
        metadata={
            "description": (
                "Constant value used when the text strategy is "
                "'constant'."
            ),
            "feature": "Text Imputation",
        },
    )

    text_strategy: Literal[
        "mode",
        "constant",
        "empty",
    ] = field(
        default="mode",
        metadata={
            "description": (
                "Strategy used to fill missing values in text columns."
            ),
            "feature": "Text Imputation",
        },
    )

 #   constant_value: str | int | float | bool | None = field(
 #       default=None,
 #       metadata={
 #           "description": (
 #               "Constant value used when a strategy is set to "
 #               "'constant'."
 #           ),
 #           "feature": "Constant Imputation",
 #       },
 #   )