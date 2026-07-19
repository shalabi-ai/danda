from __future__ import annotations

import pandas as pd
from danda.plugins.analysis.analysis_plugin import AnalysisPlugin
from danda.plugins.analysis.outlier_detector import OutlierDetector
from danda.plugins.report_collector import ReportCollector

class OutlierReportPlugin(AnalysisPlugin):
    """
    Analyzes numeric columns for outliers without modifying the DataFrame. Outliers are detected using the configured detection method (IQR, Z-score, or Modified Z-score). For each column containing outliers, the plugin reports the detection method, threshold, number and percentage of outliers, observed outlier range, calculated lower and upper bounds, an ASCII visualization of the detection interval, and optionally a sample of outlier values. When a sufficiently large dataset contains a high percentage of outliers, the report also includes a note indicating that the data may be naturally skewed rather than erroneous.

    Plugin Configuration:
    - outlier_enabled
    - outlier_method
    - outlier_iqr_multiplier
    - outlier_zscore_threshold
    - outlier_include_examples
    - outlier_max_examples
    - outlier_note_threshold

    Example:

    input:
    pd.DataFrame({
        "Age": [25, 28, 30, 27, 29, 120],
        "Salary": [50000, 52000, 51000, 49500, 50500, 51500],
        "Score": [80, 82, 81, 83, 79, 20]
    })

    Assume the configuration is:
    - outlier_method = "iqr"
    - outlier_iqr_multiplier = 1.5
    - outlier_include_examples = True
    - outlier_max_examples = 3
    - outlier_note_threshold = 10.0

    output:
    pd.DataFrame({
        "Age": [25, 28, 30, 27, 29, 120],
        "Salary": [50000, 52000, 51000, 49500, 50500, 51500],
        "Score": [80, 82, 81, 83, 79, 20]
    })

    report:
    {
        "analysis": {
            "OutlierReport": {
                "Age": {
                    "method": "IQR",
                    "threshold": "±1.5",
                    "count": 1,
                    "rows": 6,
                    "percent": 16.7,
                    "min": 120,
                    "max": 120,
                    "high_outliers": 33.75,
                    "low_outliers": 21.75,
                    "note_threshold": False,
                    "plot": [
                        "25                                           120",
                        "<=====|----------------------------------------",
                        "      UB"
                    ],
                    "examples": [
                        {
                            "index": 5,
                            "value": 120
                        }
                    ]
                }
            }
        }
    }
    """

    def __init__(self, report: ReportCollector) -> None:
        super().__init__("OutlierReport", report)

    def _execute(
        self,
        df: pd.DataFrame,
        report: ReportCollector,
    ) -> pd.DataFrame:
        return df

    def _get_report_data(
        self,
        before: pd.DataFrame,
        after: pd.DataFrame,
        report: ReportCollector,
    ) -> dict:

        config = self._get_config(before)

        method = config.analysis.outlier_method
        max_examples = config.analysis.outlier_max_examples
        include_examples = config.analysis.outlier_include_examples
        iqr_multiplier = config.analysis.outlier_iqr_multiplier
        zscore_threshold = config.analysis.outlier_zscore_threshold
        note_threshold = config.analysis.outlier_note_threshold

        result = {}

        numeric = before.select_dtypes(include="number")
        rows = len(before)

        threshold = f"×{zscore_threshold}"
        if method == "iqr":
            threshold = f"±{iqr_multiplier}"

        for column in numeric.columns:

            series = numeric[column].dropna()

            if len(series) < 2:
                continue

            mask, lower, upper = OutlierDetector.detect(series, method, iqr_multiplier, zscore_threshold)

            outliers = series[mask]

            if outliers.empty:
                continue



            percent = len(outliers) * 100 / rows
            data = {
                "method": method.upper(),
                "threshold": threshold,
                "count": len(outliers),
                "rows": rows,
                "percent": percent,
                "min": outliers.min(),
                "max": outliers.max(),
                "high_outliers": upper,
                "low_outliers": lower,
                "note_threshold": rows>=30 and percent >= note_threshold,
                "plot": OutlierDetector.outlier_graph(series, method, iqr_multiplier, zscore_threshold)
            }

            if include_examples:
                data["examples"] = [
                    {
                        "index": index,
                        "value": value,
                    }
                    for index, value in outliers.iloc[:max_examples].items()
                ]

            result[column] = data

        sorted_items = sorted(
            result.items(),
            key=lambda item: (
                -item[1]["percent"],
                item[0],  # alphabetical tie-breaker
            ),
        )
        sorted_result = dict(sorted_items)
        return sorted_result

    def _report(self, data, report: ReportCollector) -> str:

        if not data:
            return "No outliers detected."

        lines = [
            "Outliers detected:",
            "",
            "Legend:",
            "<  Bound lies below observed values",
            ">  Bound lies above observed values",
            "=  Values within normal bounds",
            "-  Outlier region",
            "|  Outlier threshold",
        ]

        for column, stats in data.items():


            lines.extend(
                [
                    "",
                    column,
                    f"Method: {stats['method']} ({stats['threshold']})",
                    f"Outliers: {self._fmt(stats['count'])} of {self._fmt(stats['rows'])} ({self._fmt(stats['percent'])}%)",
                    f"Outlier Interval: {self._fmt(stats['min'])} to {self._fmt(stats['max'])}",
                    "",
                    "Bounds:",
                    f"Lower: {self._fmt(stats['low_outliers'])}",
                    f"Upper: {self._fmt(stats['high_outliers'])}",
                    "",
                    #f"{stats['plot']}"
                ]
            )
            lines.extend(stats['plot'])

            examples = stats.get("examples")

            if examples:
                lines.append("Examples:")

                for example in examples:
                    lines.append(
                        f"- Row {example['index']}: {example['value']}"
                    )

                remaining = stats["count"] - len(examples)

                if remaining > 0:
                    lines.append(f"... {remaining} more")

            if stats["note_threshold"]:
                lines.extend(
                    [
                        "",
                        "Note:",
                        (
                            "A relatively large proportion of values were "
                            "classified as outliers."
                        ),
                        (
                            "This may indicate a skewed distribution rather "
                            "than data quality issues."
                        ),
                    ]
                )

        return "\n".join(lines)

    def _get_config_params(self, df: pd.DataFrame) -> dict:

        config = self._get_config(df).analysis

        return {
            "enabled": config.outlier_enabled,
        }