import pandas as pd


class OutlierDetector:
    """
    Detects outliers in a numeric pandas Series using one of three supported methods:

    - **IQR (Interquartile Range):** Values outside the interval
      `[Q1 - iqr_multiplier × IQR, Q3 + iqr_multiplier × IQR]`
      are considered outliers.
    - **Z-score:** Values outside
      `[mean - zscore_threshold × std, mean + zscore_threshold × std]`
      are considered outliers.
    - **Modified Z-score:** Uses the median as the center while applying the standard deviation as the spread. Values outside
      `[median - zscore_threshold × std, median + zscore_threshold × std]`
      are considered outliers.

    The detector returns:
    - a boolean mask indicating which values are outliers,
    - the calculated lower bound,
    - the calculated upper bound.

    The `outlier_graph()` helper generates a simple ASCII visualization showing the observed data range together with the calculated lower (LB) and upper (UB) outlier boundaries.

    Configuration:
    - method (`"iqr"`, `"zscore"`, or `"modified-zscore"`)
    - iqr_multiplier
    - zscore_threshold

    Example:

    input:
    pd.Series([10, 12, 11, 13, 12, 100])

    Assume the configuration is:
    - method = "iqr"
    - iqr_multiplier = 1.5
    - zscore_threshold = 3.0

    output:

    mask:
    pd.Series([False, False, False, False, False, True])

    lower_bound:
    8.5

    upper_bound:
    16.5

    graph:
    [
        "10                                          100",
        "<=====|----------------------------------------",
        "      UB"
    ]
    """

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