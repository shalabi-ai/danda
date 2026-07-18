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

    import pandas as pd

    def outlier_graph(
        series: pd.Series,
        method: str = "iqr",
        iqr_multiplier: float = 1.5,
        zscore_threshold: float = 3.0,
        width: int = 50,
    ) -> list:
        """
        Return an ASCII visualization of the outlier bounds.

        Example:

        43                    58.75              64.75                    79
        |----------------------|==================|------------------------|
                               LB                UB
        """

        mask, lower, upper = OutlierDetector.detect(
            series,
            method=method,
            iqr_multiplier=iqr_multiplier,
            zscore_threshold=zscore_threshold,
        )

        valid = series.dropna()

        if valid.empty:
            return "No numeric data."

        observed_min = valid.min()
        observed_max = valid.max()

        # Degenerate case
        if observed_min == observed_max:
            return f"{observed_min}\n{'|' + '=' * (width - 2) + '|'}"

        def pos(value: float) -> int:
            value = max(observed_min, min(observed_max, value))
            return round(
                (value - observed_min) / (observed_max - observed_min) * (width - 1)
            )

        lo = pos(lower)
        hi = pos(upper)

        graph = ["-"] * width

        # Normal range
        for i in range(lo, hi + 1):
            graph[i] = "="

        # Bounds
        graph[lo] = "|"
        graph[hi] = "|"

        line = "".join(graph)

        header = (
            f"{observed_min:g}"
            + " " * max(1, width - len(f"{observed_min:g}") - len(f"{observed_max:g}"))
            + f"{observed_max:g}"
        )

        labels = [" "] * width
        for text, p in [("LB", lo), ("UB", hi)]:
            start = max(0, min(width - len(text), p - len(text) // 2))
            labels[start : start + len(text)] = list(text)

        label_line = "".join(labels)

        #return f"{header}\n{line}\n{label_line}"
        return [header, line, label_line]