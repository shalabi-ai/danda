# analyze

Analyze the DataFrame and generate data quality reports.

This method performs non-destructive analysis only. The returned
DataFrame is unchanged, but a collection of analysis reports is
attached to the DataFrame metadata.

The analysis includes:

- Column summary statistics.
- Missing-value summary.
- Detailed missing-value report.
- Detection of potential missing-value placeholders.
- Detection of suspicious missing-value patterns.
- Sparse row analysis.
- Detection of potential boolean columns.
- Detection of constant columns.
- Outlier analysis.

Returns
-------
pandas.DataFrame
    The original DataFrame with attached analysis reports.

Notes
-----
No values, columns, or dtypes are modified.

The analysis report is stored in::

    df.attrs["danda_analyze_report"]

and can be accessed using::

    df.dg.report["analyze"]

Examples
--------
>>> df = pd.read_csv("customers.csv")
>>> df = df.dg.analyze()
>>> df.dg.report["analyze"]



## ColumnSummaryPlugin

Generates a summary of every column in the DataFrame without modifying the data. For each column, the plugin reports the data type, the number and percentage of missing values, and the number of unique non-missing values.

### Configuration

- None (always enabled)

### Example

input:
pd.DataFrame({
    "Name": ["Alice", "Bob", None, "Alice"],
    "Age": [25, 30, None, 25],
    "City": ["London", "Paris", "Paris", None]
})

output:
pd.DataFrame({
    "Name": ["Alice", "Bob", None, "Alice"],
    "Age": [25, 30, None, 25],
    "City": ["London", "Paris", "Paris", None]
})

report:
{
    "analysis": {
        "ColumnSummaryPlugin": {
            "Name": {
                "dtype": "object",
                "missing": 1,
                "missing_percent": 25,
                "unique": 2
            },
            "Age": {
                "dtype": "float64",
                "missing": 1,
                "missing_percent": 25,
                "unique": 2
            },
            "City": {
                "dtype": "object",
                "missing": 1,
                "missing_percent": 25,
                "unique": 2
            }
        }
    }
}


## MissingValuesSummaryPlugin

Provides an overall summary of missing values in the DataFrame without modifying the data. The summary includes the total number of rows and columns, the number and percentage of missing cells, the number of columns containing missing values, the number of rows containing missing values, and the number and percentage of complete rows.

### Configuration

- None (always enabled)

### Example

input:
pd.DataFrame({
    "Name": ["Alice", None, "Charlie", "David"],
    "Age": [25, None, 35, 40],
    "City": ["London", "Paris", None, None]
})

output:
pd.DataFrame({
    "Name": ["Alice", None, "Charlie", "David"],
    "Age": [25, None, 35, 40],
    "City": ["London", "Paris", None, None]
})

report:
{
    "analysis": {
        "MissingValuesSummaryPlugin": {
            "rows": 4,
            "columns": 3,
            "missing_cells": 4,
            "missing_percent": 33.3,
            "columns_with_missing": 3,
            "rows_with_missing": 3,
            "complete_rows": 1,
            "complete_rows_percent": 25.0
        }
    }
}


## MissingValuesReportPlugin

Analyzes the DataFrame and reports the number and percentage of missing values for each column containing at least one missing value. Columns without missing values are excluded from the report. The plugin performs analysis only and does not modify the input DataFrame.

### Configuration

- None (always enabled)

### Example

input:
pd.DataFrame({
    "Name": ["Alice", None, "Charlie", "David"],
    "Age": [25, None, 35, 40],
    "City": ["London", "Paris", None, None],
    "Country": ["UK", "France", "UK", "Germany"]
})

output:
pd.DataFrame({
    "Name": ["Alice", None, "Charlie", "David"],
    "Age": [25, None, 35, 40],
    "City": ["London", "Paris", None, None],
    "Country": ["UK", "France", "UK", "Germany"]
})

report:
{
    "analysis": {
        "MissingValuesReportPlugin": {
            "Name": {
                "count": 1,
                "percent": 25.0
            },
            "Age": {
                "count": 1,
                "percent": 25.0
            },
            "City": {
                "count": 2,
                "percent": 50.0
            }
        }
    }
}


## PotentialMissingValuesPlugin

Identifies string values that are likely intended to represent missing data without modifying the DataFrame. The plugin searches string columns for user-configured placeholder values (such as `"N/A"`, `"Unknown"`, or `"None"`), with optional whitespace trimming and case-insensitive matching. The report lists each column containing potential missing values together with the number of occurrences of each configured placeholder.

### Configuration

- empty_value_enabled
- empty_value_values
- empty_value_strip_whitespace
- empty_value_ignore_case

### Example

input:
pd.DataFrame({
    "Name": ["Alice", "N/A", "Bob", " unknown "],
    "City": ["London", "None", "Paris", "Berlin"],
    "Department": ["HR", "IT", "Unknown", "HR"],
    "Age": [25, 30, 35, 40]
})

Assume the configuration is:
- empty_value_values = ["N/A", "None", "Unknown"]
- empty_value_strip_whitespace = True
- empty_value_ignore_case = True

output:
pd.DataFrame({
    "Name": ["Alice", "N/A", "Bob", " unknown "],
    "City": ["London", "None", "Paris", "Berlin"],
    "Department": ["HR", "IT", "Unknown", "HR"],
    "Age": [25, 30, 35, 40]
})

report:
{
    "analysis": {
        "PotentialMissingValuesPlugin": {
            "Name": {
                "N/A": 1,
                "Unknown": 1
            },
            "City": {
                "None": 1
            },
            "Department": {
                "Unknown": 1
            }
        }
    }
}


## SuspiciousMissingValuesPlugin

Identifies values that may indicate missing data without modifying the DataFrame. The plugin searches all columns for user-configured suspicious values, such as placeholders like `"?"`, `"-"`, `"Unknown"`, `"Missing"`, or other domain-specific indicators. Matching can optionally ignore letter casing and leading/trailing whitespace. The report lists each column containing suspicious values together with the number of occurrences of each detected indicator.

### Configuration

- suspicious_missing_enabled
- suspicious_missing_values
- suspicious_missing_ignore_case
- suspicious_missing_strip_whitespace

### Example

input:
pd.DataFrame({
    "Name": ["Alice", "Unknown", "Bob", " Missing "],
    "City": ["London", "?", "Paris", "-"],
    "Department": ["HR", "IT", "Unknown", "HR"],
    "Age": [25, 30, 35, 40]
})

Assume the configuration is:
- suspicious_missing_values = ["Unknown", "Missing", "?", "-"]
- suspicious_missing_ignore_case = True
- suspicious_missing_strip_whitespace = True

output:
pd.DataFrame({
    "Name": ["Alice", "Unknown", "Bob", " Missing "],
    "City": ["London", "?", "Paris", "-"],
    "Department": ["HR", "IT", "Unknown", "HR"],
    "Age": [25, 30, 35, 40]
})

report:
{
    "analysis": {
        "SuspiciousMissingValuesPlugin": {
            "Name": {
                "Unknown": 1,
                "Missing": 1
            },
            "City": {
                "?": 1,
                "-": 1
            },
            "Department": {
                "Unknown": 1
            }
        }
    }
}


## SparseRowsReportPlugin

Identifies rows containing a high proportion of missing values without modifying the DataFrame. A row is reported when the fraction of missing values is greater than or equal to the configured threshold. The report includes the row index, the number of missing values, the total number of columns, and the percentage of missing values. Results are sorted by missing percentage (highest first) and limited to the configured maximum number of rows.

### Configuration

- sparse_rows_report_enabled
- sparse_rows_report_threshold
- sparse_rows_report_max_rows

### Example

input:
pd.DataFrame({
    "A": [1, None, None, 4],
    "B": [2, None, None, None],
    "C": [3, None, 5, None],
    "D": [4, None, None, 8]
})

Assume the configuration is:
- sparse_rows_report_threshold = 0.75
- sparse_rows_report_max_rows = 10

output:
pd.DataFrame({
    "A": [1, None, None, 4],
    "B": [2, None, None, None],
    "C": [3, None, 5, None],
    "D": [4, None, None, 8]
})

report:
{
    "analysis": {
        "SparseRowsReportPlugin": [
            {
                "index": 1,
                "missing": 4,
                "total": 4,
                "percent": 100.0
            },
            {
                "index": 2,
                "missing": 3,
                "total": 4,
                "percent": 75.0
            },
            {
                "index": 3,
                "missing": 2,
                "total": 4,
                "percent": 50.0
            }
        ]
    }
}


## PotentialBooleanTypePlugin

Identifies columns that may represent boolean values but are not in a recognized boolean format. A column is reported when it contains exactly two distinct non-missing values and those values are not already one of the supported boolean representations (`True`, `False`, `0`, `1`, `"true"`, `"false"`, `"0"`, or `"1"`). The plugin performs analysis only and does not modify the input DataFrame.

### Configuration

- potential_boolean_enabled

### Example

input:
pd.DataFrame({
    "Subscribed": ["Yes", "No", "Yes", "No"],
    "Approved": ["Y", "N", "Y", "N"],
    "IsActive": ["true", "false", "true", "false"],
    "Status": ["Open", "Closed", "Pending", "Open"]
})

output:
pd.DataFrame({
    "Subscribed": ["Yes", "No", "Yes", "No"],
    "Approved": ["Y", "N", "Y", "N"],
    "IsActive": ["true", "false", "true", "false"],
    "Status": ["Open", "Closed", "Pending", "Open"]
})

report:
{
    "analysis": {
        "PotentialBooleanTypePlugin": {
            "Subscribed": ["Yes", "No"],
            "Approved": ["Y", "N"]
        }
    }
}


## ConstantColumnsPlugin

Identifies columns whose non-missing values are all identical. A column is considered constant if it contains exactly one unique non-null value, regardless of the number of missing values. The plugin performs analysis only and does not modify the input DataFrame.

### Configuration

- None (always enabled)

### Example

input:
pd.DataFrame({
    "Country": ["USA", "USA", "USA", None],
    "Status": ["Active", "Inactive", "Active", "Inactive"],
    "Version": [1, 1, 1, 1],
    "Score": [10, 20, 30, 40]
})

output:
pd.DataFrame({
    "Country": ["USA", "USA", "USA", None],
    "Status": ["Active", "Inactive", "Active", "Inactive"],
    "Version": [1, 1, 1, 1],
    "Score": [10, 20, 30, 40]
})

report:
{
    "analysis": {
        "ConstantColumns": {
            "Country": "USA",
            "Version": 1
        }
    }
}


## OutlierReportPlugin

Analyzes numeric columns for outliers without modifying the DataFrame. Outliers are detected using the configured detection method (IQR, Z-score, or Modified Z-score). For each column containing outliers, the plugin reports the detection method, threshold, number and percentage of outliers, observed outlier range, calculated lower and upper bounds, an ASCII visualization of the detection interval, and optionally a sample of outlier values. When a sufficiently large dataset contains a high percentage of outliers, the report also includes a note indicating that the data may be naturally skewed rather than erroneous.

### Configuration

- outlier_enabled
- outlier_method
- outlier_iqr_multiplier
- outlier_zscore_threshold
- outlier_include_examples
- outlier_max_examples
- outlier_note_threshold

### Example

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
