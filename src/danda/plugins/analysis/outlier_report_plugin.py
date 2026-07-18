from __future__ import annotations

import pandas as pd
from danda.plugins.analysis.analysis_plugin import AnalysisPlugin
from danda.plugins.analysis.outlier_detector import OutlierDetector
from danda.plugins.report_collector import ReportCollector

class OutlierReportPlugin(AnalysisPlugin):

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
                "note_threshold": percent >= note_threshold,
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

        lines = ["Outliers detected:"]

        for column, stats in data.items():


            lines.extend(
                [
                    "",
                    column,
                    f"Method: {stats['method']} ({stats['threshold']})",
                    f"Outliers: {self._fmt(stats['count'])} of {self._fmt(stats['rows'])} ({self._fmt(stats['percent'])}%)",
                    f"Outlier Range: {self._fmt(stats['min'])} to {self._fmt(stats['max'])}",
                    "",
                    "Bounds:",
                    f"Lower: {self._fmt(stats['low_outliers'])}",
                    f"Upper: {self._fmt(stats['high_outliers'])}",
                ]
            )

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