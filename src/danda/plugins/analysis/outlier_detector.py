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

        elif method == "modified-zscore":

            mean = valid.median()
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

    import pandas as pd

    def outlier_graph(
        series: pd.Series,
        method: str = "iqr",
        iqr_multiplier: float = 1.5,
        zscore_threshold: float = 3.0,
        width: int = 50,
    ) -> list:

        _, lower, upper = OutlierDetector.detect(
            series,
            method,
            iqr_multiplier,
            zscore_threshold,
        )

        valid = series.dropna()

        if valid.empty:
            return []

        observed_min = valid.min()
        observed_max = valid.max()

        if observed_min == observed_max:
            return [f"{observed_min:g}\n|{'=' * (width - 2)}|"]

        def pos(value: float) -> int:
            return round(
                (value - observed_min) / (observed_max - observed_min) * (width - 1)
            )

        lo_outside = lower < observed_min
        hi_outside = upper > observed_max

        lo = 0 if lo_outside else pos(lower)
        hi = width - 1 if hi_outside else pos(upper)

        graph = ["-"] * width

        for i in range(lo, hi + 1):
            graph[i] = "="

        if lo_outside:
            graph[0] = "<"
        else:
            graph[lo] = "|"

        if hi_outside:
            graph[-1] = ">"
        else:
            graph[hi] = "|"

        header = (
            f"{observed_min:g}"
            + " " * max(1, width - len(f"{observed_min:g}") - len(f"{observed_max:g}"))
            + f"{observed_max:g}"
        )

        labels = [" "] * width

        if not lo_outside:
            labels[max(0, lo - 1) : max(0, lo - 1) + 2] = "LB"

        if not hi_outside:
            start = min(width - 2, hi - 1)
            labels[start : start + 2] = "UB"

        return ["".join(header), "".join(graph), "".join(labels)]