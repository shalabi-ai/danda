# Imputation Guide

`danda` can automatically fill missing values using deterministic, configurable strategies.

Unlike cleaning operations, **imputation modifies the contents of the DataFrame** by replacing missing values with inferred values. Because this may affect subsequent analysis, imputation is **disabled by default** and must be explicitly enabled.

---

# Philosophy

Danda's primary goal is to prepare data for analysis using transformations that are:

* Objective
* Safe
* Deterministic
* Automatic

Imputation is different.

Replacing missing values requires assumptions about the data, so Danda never performs it automatically. Instead, it provides simple, transparent strategies that users can explicitly enable.

---

# Enabling Imputation

```python
import danda
import pandas as pd

df = pd.read_csv("employees.csv")

df.dg.config.imputation.enabled = True

df = df.dg.impute()
```

A typical workflow is

```python
df = (
    pd.read_csv("employees.csv")
      .dg.clean()
      .dg.optimize()
      .dg.impute()
)
```

where

* `clean()` removes objectively bad data,
* `optimize()` converts columns to appropriate data types,
* `impute()` fills missing values.

Running `optimize()` before `impute()` is recommended because it allows Danda to select strategies based on the correct column data types.

---

# Default Strategies

| Data Type | Default Strategy |
| --------- | ---------------- |
| Numeric   | `median`         |
| Boolean   | `mode`           |
| Category  | `mode`           |
| Text      | `mode`           |
| Datetime  | `ffill`          |

---

# Numeric Columns

Supported strategies:

* `median`
* `mean`
* `mode`
* `constant`

Example

Before

```text
Age
----
20
22
NaN
30
```

Using

```python
df.dg.config.imputation.numeric_strategy = "median"
```

After

```text
Age
----
20
22
22
30
```

---

# Boolean Columns

Supported strategies:

* `mode`
* `constant`

Example

Before

```text
Approved
--------
True
False
NaN
True
```

After (`mode`)

```text
Approved
--------
True
False
True
True
```

---

# Categorical Columns

Supported strategies:

* `mode`
* `constant`

Example

Before

```text
Country
-------
USA
Canada
NaN
USA
```

After (`mode`)

```text
Country
-------
USA
Canada
USA
USA
```

When using the `constant` strategy, Danda automatically adds the constant to the category if necessary.

---

# Text Columns

Supported strategies:

* `mode`
* `constant`
* `empty`

Example

Before

```text
City
----
Berlin
NaN
Berlin
Paris
```

After (`mode`)

```text
City
----
Berlin
Berlin
Berlin
Paris
```

The `empty` strategy replaces missing values with an empty string.

---

# Datetime Columns

Supported strategies:

* `ffill`
* `bfill`
* `constant`

Forward fill

```text
2024-01-01
NaT
NaT
2024-01-04
```

↓

```text
2024-01-01
2024-01-01
2024-01-01
2024-01-04
```

Backward fill

```text
2024-01-01
NaT
NaT
2024-01-04
```

↓

```text
2024-01-01
2024-01-04
2024-01-04
2024-01-04
```

---

# Configuration

```python
df.dg.config.imputation.enabled = True

df.dg.config.imputation.numeric_strategy = "median"
df.dg.config.imputation.boolean_strategy = "mode"
df.dg.config.imputation.category_strategy = "mode"
df.dg.config.imputation.text_strategy = "mode"
df.dg.config.imputation.datetime_strategy = "ffill"

df.dg.config.imputation.constant_value = "Unknown"
```

---

# Reporting

Every imputation operation is recorded.

Example

```text
Filled missing values:
- Age: median (12)
- Salary: mean (4)
- Country: mode (8)
- Date: ffill (2)
```

The structured report is also available through

```python
df.dg.report
```

---

# Notes

* Imputation only affects missing values (`NaN`, `None`, `NaT`, and values normalized by `clean()`).
* Columns without missing values are left unchanged.
* Existing data is never modified.
* The original DataFrame is never modified; `impute()` returns a new DataFrame.

---

# Best Practices

For most datasets, the recommended workflow is

```python
df = (
    pd.read_csv("data.csv")
      .dg.clean()
      .dg.optimize()
      .dg.impute()
)
```

This ensures that:

1. Missing value indicators are normalized.
2. Empty rows and columns are removed.
3. Columns are converted to appropriate data types.
4. Missing values are filled using strategies appropriate for each data type.

---

# Limitations

Danda intentionally provides only simple, deterministic imputation strategies.

It does **not** implement model-based methods such as:

* K-Nearest Neighbors (KNN)
* Multiple Imputation by Chained Equations (MICE)
* Regression-based imputation
* Random Forest imputation
* Deep learning-based imputation

These methods require statistical assumptions and are better handled by dedicated machine learning libraries such as scikit-learn.
