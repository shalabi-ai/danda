import pandas as pd


class OutlierDetector:

    @staticmethod
    def detect(
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