from __future__ import annotations

from typing import Literal

import pandas as pd

from danda.plugins.analysis.outlier_detector import OutlierDetector


class DandaActionAccessor:

    def __init__(self, df: pd.DataFrame):
        self._df = df

    def handle_outliers(
        self,
        columns: list[str] | None = None,
        *,
        method: Literal["iqr", "zscore", "modified-zscore"] = "modified-zscore",
        strategy: Literal["remove", "nan", "clip", "mask"] = "remove",
        iqr_multiplier: float = 1.5,
        zscore_threshold: float = 3.0,
    ) -> pd.DataFrame:

        if not columns:
            return self._df

        df = self._df.copy()

        row_mask = pd.Series(False, index=df.index)
        mask_df = pd.DataFrame()

        for column in columns:

            if column not in df.columns:
                raise KeyError(f"Column '{column}' does not exist.")

            if not pd.api.types.is_numeric_dtype(df[column]):
                raise TypeError(f"Column '{column}' must be numeric.")

            series = df[column]

            mask, lower, upper = OutlierDetector.detect( #self._detect_outliers(
                series,
                method,
                iqr_multiplier,
                zscore_threshold,
            )

            if strategy == "remove":  # removes whole rows
                row_mask |= mask

            elif strategy == "nan":  # nan only affects offending values
                df.loc[mask, column] = pd.NA

            elif strategy == "clip":  # clip is column-wise
                df[column] = series.clip(lower=lower, upper=upper)

            elif strategy == "mask":
                mask_df[column] = mask.copy()

            else:
                raise ValueError(
                    f"Unknown strategy '{strategy}'."
                )

        if strategy == "remove":
            df = df.loc[~row_mask].copy()

        if strategy == "mask":
            return mask_df

        return df

