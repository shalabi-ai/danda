from __future__ import annotations

import pandas as pd

from danda.plugins.analysis.analysis_plugin import AnalysisPlugin
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

        result = {}

        numeric = before.select_dtypes(include="number")

        for column in numeric.columns:

            series = numeric[column].dropna()

            if len(series) < 2:
                continue

            if method == "iqr":
                mask = self._iqr_mask(
                    series,
                    config.analysis.outlier_iqr_multiplier,
                )

            elif method == "zscore":
                mask = self._zscore_mask(
                    series,
                    config.analysis.outlier_zscore_threshold,
                )

            else:
                raise ValueError(f"Unknown outlier method: {method}")

            outliers = series[mask]

            if outliers.empty:
                continue

            data = {
                "method": method.upper(),
                "count": len(outliers),
                "min": outliers.min(),
                "max": outliers.max(),
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

        return result

    def _iqr_mask(
        self,
        series: pd.Series,
        multiplier: float,
    ) -> pd.Series:

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)

        iqr = q3 - q1

        lower = q1 - multiplier * iqr
        upper = q3 + multiplier * iqr

        return (series < lower) | (series > upper)

    def _zscore_mask(
        self,
        series: pd.Series,
        threshold: float,
    ) -> pd.Series:

        std = series.std()

        if std == 0:
            return pd.Series(False, index=series.index)

        z = (series - series.mean()) / std

        return z.abs() > threshold

    def _report(self, data, report: ReportCollector) -> str:

        if not data:
            return "No outliers detected."

        lines = ["Outliers detected:"]

        for column, stats in data.items():

            lines.extend(
                [
                    "",
                    column,
                    f"Method: {stats['method']}",
                    f"Outliers: {stats['count']}",
                    f"Range: {stats['min']} to {stats['max']}",
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

        return "\n".join(lines)

    def _get_config_params(self, df: pd.DataFrame) -> dict:

        config = self._get_config(df).analysis

        return {
            "enabled": config.outlier_enabled,
        }