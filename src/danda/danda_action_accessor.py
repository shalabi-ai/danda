from __future__ import annotations

from typing import Literal

import pandas as pd


class DandaActionAccessor:

    def __init__(self, df: pd.DataFrame):
        self._df = df

    def handle_outliers(
        self,
        columns: list[str] | None = None,
        *,
        method: Literal["iqr", "zscore"] = "iqr",
        strategy: Literal["remove", "nan", "clip"] = "remove",
        iqr_multiplier: float = 1.5,
        zscore_threshold: float = 3.0,
    ) -> pd.DataFrame:

        if not columns or len(columns) == 0:
            return self._df

        df = self._df.copy()

        row_mask = pd.Series(False, index=df.index)

        for column in columns:

            if column not in df.columns:
                raise KeyError(f"Column '{column}' does not exist.")

            if not pd.api.types.is_numeric_dtype(df[column]):
                raise TypeError(f"Column '{column}' must be numeric.")

            series = df[column]

            mask, lower, upper = self._detect_outliers(
                series,
                method,
                iqr_multiplier,
                zscore_threshold,
            )

            if strategy == "remove":
                row_mask |= mask

            elif strategy == "nan":
                df.loc[mask, column] = pd.NA

            elif strategy == "clip":
                df[column] = series.clip(lower=lower, upper=upper)

            else:
                raise ValueError(
                    f"Unknown strategy '{strategy}'."
                )

        if strategy == "remove":
            df = df.loc[~row_mask].copy()

        return df

    @staticmethod
    def _detect_outliers(
        series: pd.Series,
        method: str,
        iqr_multiplier: float,
        zscore_threshold: float,
    ) -> tuple[pd.Series, float, float]:

        valid = series.dropna()

        if valid.empty:
            return (
                pd.Series(False, index=series.index),
                float("-inf"),
                float("inf"),
            )

        if method == "iqr":

            q1 = valid.quantile(0.25)
            q3 = valid.quantile(0.75)

            iqr = q3 - q1

            lower = q1 - iqr_multiplier * iqr
            upper = q3 + iqr_multiplier * iqr

        elif method == "zscore":

            mean = valid.mean()
            std = valid.std()

            if std == 0:
                return (
                    pd.Series(False, index=series.index),
                    float("-inf"),
                    float("inf"),
                )

            lower = mean - zscore_threshold * std
            upper = mean + zscore_threshold * std

        else:
            raise ValueError(f"Unknown method '{method}'.")

        mask = (series < lower) | (series > upper)

        return mask.fillna(False), lower, upper

