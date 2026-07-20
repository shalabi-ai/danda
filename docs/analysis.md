# Data Analysis

`danda` provides a collection of **analysis plugins** that inspect your DataFrame and generate human-readable reports. Unlike cleaning or optimization plugins, analysis plugins **never modify the data**—they only provide insight into its quality and structure.

```python
report = df.dg.analyze()
print(report.dg.report["analysis"])
```

Analysis reports are designed to be:

- **Objective** – based on measurable characteristics of the data.
- **Safe** – never change the DataFrame.
- **Actionable** – help you decide what to clean or investigate.

---

# Data Overview

## Column Summary

Provides a high-level summary of every column.

Example:

```text
Age
Type: float64
Missing: 177
Unique: 88

Sex
Type: category
Missing: 0
Unique: 2
```

Useful for quickly understanding the structure of a dataset.

---

## Constant Columns

Reports columns that contain only a single unique value.

Example:

```text
Constant columns detected:

PassengerClass
Value: Third

Country
Value: USA
```

Constant columns often provide little analytical value and may be candidates for removal.

---

# Missing Data Analysis

## Missing Values Summary

Provides an overall summary of missing values in the DataFrame.

Example:

```text
Rows: 891
Columns: 12

Columns with missing values: 3
Total missing values: 866
```

---

## Missing Values Report

Reports missing values for each column.

Example:

```text
Missing values detected:

Age: 177 (19.9%)
Cabin: 687 (77.1%)
Embarked: 2 (0.2%)
```

Columns are sorted by the percentage of missing values.

---

## Potential Missing Values

Detects text values that commonly represent missing data but are **not automatically converted** to `NaN`.

By default, danda looks for:

```text
n/a
na
?
-
--
```

Example:

```text
Potential missing values detected:

Status
- "N/A": 18
- "?": 5

Comment
- "--": 3
```

### Configuration

```python
config = df.dg.config.analysis

config.empty_value_enabled = True

config.empty_value_values = (
    "n/a",
    "?",
    "-",
)

config.empty_value_ignore_case = True
config.empty_value_strip_whitespace = True
```

---

## Suspicious Missing Values

Reports values commonly used as sentinel values for missing data.

Default values include:

```text
-9999
-999
999
9999
99999
2147483647
-1
UNKNOWN
MISSING
TBD
TBA
PENDING
```

Example:

```text
Suspicious missing values detected:

Temperature
-9999: 14

Status
UNKNOWN: 27
```

These values are **reported only**—they are never automatically converted.

### Configuration

```python
config = df.dg.config.analysis

config.suspicious_missing_enabled = True

config.suspicious_missing_values = (
    -999,
    -1,
    "UNKNOWN",
    "MISSING",
)

config.suspicious_missing_ignore_case = True
config.suspicious_missing_strip_whitespace = True
```

---

# Sparse Data

## Sparse Rows Report

Reports rows containing a high proportion of missing values.

Example:

```text
Sparse rows detected:

Row 42
Missing: 10 of 12 columns (83%)

Row 181
Missing: 9 of 12 columns (75%)
```

Useful for identifying rows that may need further investigation or removal.

### Configuration

```python
config = df.dg.config.analysis

config.sparse_rows_report_enabled = True

config.sparse_rows_report_threshold = 0.5
config.sparse_rows_report_max_rows = 20
```

| Setting | Description |
|----------|-------------|
| `sparse_rows_report_threshold` | Minimum proportion of missing values required for a row to be reported. |
| `sparse_rows_report_max_rows` | Maximum number of rows shown in the report. |

---

# Type Analysis

## Potential Boolean Columns

Detects columns that appear to contain boolean values but have not yet been converted.

Example:

```text
Potential boolean columns:

Purchased

Values:
Yes
No

Subscribed

Values:
True
False
```

This helps identify columns that can be converted using `df.dg.optimize()`.

---

# Outlier Detection

Reports statistical outliers for numeric columns.

Supported methods:

- IQR (Interquartile Range)
- Z-score

Example:

```text
price
Method: IQR

Outliers: 3,523 of 53,794 (6.5%)

Outlier Range:
11,897 to 18,823

Bounds:
Lower: -5,612.62
Upper: 11,890.38

Examples:
- Row 23825: 11897
- Row 23826: 11899
...
```

If a relatively large proportion of values are classified as outliers, danda includes an informational note:

```text
Note:
A relatively large proportion of values were classified as outliers.
This may indicate a skewed distribution rather than data quality issues.
```

The report is **descriptive only** and never removes or modifies values.

## Configuration

Enable or disable outlier detection:

```python
config = df.dg.config.analysis

config.outlier_enabled = True
```

### Detection method

Use the Interquartile Range method:

```python
config.outlier_method = "iqr"
```

or the Z-score method:

```python
config.outlier_method = "zscore"
```

### IQR configuration

```python
config.outlier_iqr_multiplier = 1.5
```

Larger multipliers classify fewer values as outliers.

### Z-score configuration

```python
config.outlier_zscore_threshold = 3.0
```

Larger thresholds classify fewer values as outliers.

### Report examples

Control whether example values are shown.

```python
config.outlier_include_examples = True
config.outlier_max_examples = 10
```

Example output:

```text
Examples:
- Row 104: 152
- Row 201: 168
...
```

### Skewness note

Control when the informational note is displayed.

```python
config.outlier_note_threshold = 5.0
```

If more than 5% of values in a column are classified as outliers, the report includes a note indicating that the distribution may be naturally skewed.

---

# Example

Customize several analysis plugins:

```python
config = df.dg.config.analysis

config.empty_value_values = ("n/a", "unknown", "?")

config.suspicious_missing_values = (
    -999,
    "UNKNOWN",
)

config.sparse_rows_report_threshold = 0.6

config.outlier_method = "zscore"
config.outlier_zscore_threshold = 2.5
config.outlier_include_examples = True
config.outlier_max_examples = 5
```

Then run the analysis:

```python
report = df.dg.analyze()

print(report.dg.report["analysis"])
```

Analysis plugins never modify your DataFrame. They provide objective reports that help you understand the quality, completeness, and statistical characteristics of your data before deciding on any cleaning or transformation steps.
