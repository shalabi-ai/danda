# danda

> **_Stop writing the same pandas preprocessing code over and over._**
> 
> **Automatically clean and optimize pandas DataFrames with one line of code.**
> 
> **Prepare your pandas DataFrames for analysis with safe, deterministic transformations.**
> 

`danda` is a lightweight extension for **pandas** that helps you clean, optimize, analyze, and impute data using a simple DataFrame accessor.

Instead of writing repetitive preprocessing code for every project, `danda` provides a consistent, configurable workflow that prepares your data for analysis while preserving its meaning.

```python
import pandas as pd
import danda

df = (
    pd.read_csv("employees.csv")
      .dg.clean()
      .dg.optimize()
)

print(df.dtypes)
print(df.dg.report)
```

---

## Philosophy

`danda` is built on a simple principle:

> **Only automate transformations that are objective, safe, and almost always desired.**

A transformation should be:

- **Objective** — there is little ambiguity about the correct result.
- **Safe** — it has a very low risk of changing the meaning of the data.
- **Automatic** — it is something users almost always perform after loading a DataFrame.

For example, `danda` will automatically:

- Remove completely empty rows and columns.
- Remove duplicate rows.
- Trim whitespace from string values.
- Normalize common missing values.
- Convert numeric strings to numeric types.
- Detect boolean values.
- Detect datetime values.
- Convert suitable string columns to categorical types.
- Reduce memory usage by selecting more efficient data types.
- Generate data quality reports.

On the other hand, operations that require domain knowledge—such as imputing missing values, removing outliers, or dropping columns—are never performed automatically. These actions require explicit user intent.

By focusing on deterministic, low-risk transformations, `danda` helps keep preprocessing code concise, reproducible, and easy to reason about while remaining fully compatible with the pandas ecosystem.

---

## Why danda?

Most data analysis projects begin with the same repetitive preprocessing steps.

```python
import pandas as pd

df = pd.read_csv("employees.csv")

# Remove empty data
df = df.dropna(how="all")
df = df.dropna(axis=1, how="all")
df = df.drop_duplicates()

# Clean strings
df = df.apply(
    lambda col: col.str.strip() if col.dtype == "object" else col
)

# Convert data types
df["age"] = pd.to_numeric(df["age"])
df["active"] = df["active"].map({"True": True, "False": False})
df["created"] = pd.to_datetime(df["created"])
df["country"] = df["country"].astype("category")
```

This code is repeated across notebooks, scripts, and projects. It is often inconsistent, difficult to maintain, and easy to forget.

With `danda`, the same workflow becomes:

```python
import pandas as pd
import danda

df = (
    pd.read_csv("employees.csv")
      .dg.clean()
      .dg.optimize()
)
```

The result is a DataFrame that is ready for analysis with minimal code while remaining entirely within the pandas API.

### Designed for safe automation

Unlike many preprocessing libraries, `danda` intentionally avoids making assumptions about your data.

It only automates operations that are:

- **Objective** — there is little ambiguity about the correct result.
- **Safe** — they are unlikely to change the meaning of the data.
- **Common** — they are operations that users almost always perform after loading a DataFrame.

For example, `danda` will automatically:

- Remove completely empty rows and columns.
- Remove duplicate rows.
- Trim whitespace from string values.
- Normalize common missing values.
- Infer numeric, boolean, datetime, and categorical types.
- Optimize memory usage.
- Generate data quality reports.

However, operations that depend on domain knowledge are never performed automatically.

For example, `danda` will **not**:

- Remove outliers.
- Impute missing values.
- Drop columns because they contain missing values.
- Encode categorical variables.
- Scale or normalize numeric data.
- Modify values based on statistical assumptions.

These tasks require explicit user intent because there is no universally correct answer.

By separating **automatic preparation** from **user-driven decisions**, `danda` provides a predictable and reproducible workflow that keeps your preprocessing code concise without sacrificing control.

---

## Installation

Install `danda` from PyPI using `pip`:

```bash
pip install danda
```

`danda` extends the pandas API by registering the `.dg` DataFrame accessor. Simply import `danda` once in your application before using the accessor.

```python
import pandas as pd
import danda

df = pd.read_csv("employees.csv")

df.dg.clean()
```

### Requirements

- Python 3.10+
- pandas 2.x

### Verify the installation

```python
import pandas as pd
import danda

df = pd.DataFrame({"A": [1, 2, 3]})

print(df.dg)
```

If the installation was successful, the `.dg` accessor will be available on every pandas `DataFrame`.

---

## Quick Start

`danda` integrates directly with pandas through the `.dg` DataFrame accessor. A typical workflow consists of four steps:

1. **Clean** the data.
2. **Optimize** data types and memory usage.
3. **Analyze** data quality.
4. **Impute** missing values (optional).

```python
import pandas as pd
import danda

df = pd.read_csv("employees.csv")

# Clean the data
df = df.dg.clean()

# Optimize data types
df = df.dg.optimize()

# Generate analysis reports
df = df.dg.analyze()

# (Optional) Impute missing values
# df = df.dg.impute()
```

### Chaining operations

Since each operation returns a new DataFrame, they can be chained together.

```python
df = (
    pd.read_csv("employees.csv")
      .dg.clean()
      .dg.optimize()
      .dg.analyze()
)
```

### Viewing reports

Most operations generate reports describing what was detected or changed.

```python
reports = df.dg.report

print(reports["clean"])
print(reports["optimize"])
print(reports["analysis"])
```

Example:

```text
Clean
├── Removed 3 empty rows
├── Removed 1 empty column
└── Removed 12 duplicate rows

Optimize
├── Converted 4 columns to numeric
├── Converted 2 columns to datetime
└── Reduced memory usage by 68%

Analysis
├── Missing values detected
├── Constant columns detected
└── Outliers detected
```

### Configuration

Every DataFrame has its own configuration, allowing you to customize `danda` without affecting other DataFrames.

```python
config = df.dg.config

config.types.datetime_enabled = False
config.analysis.outlier_method = "zscore"

df = (
    df
    .dg.clean()
    .dg.optimize()
    .dg.analyze()
)
```

This keeps your preprocessing pipeline concise, reproducible, and fully configurable while remaining entirely within the pandas API.

---

## Documentation

The README provides an overview of `danda`. Detailed documentation for each feature is available in the `docs/` directory.

| Guide                                      | Description |
|--------------------------------------------|-------------|
| **Getting Started**                        | Install `danda`, understand its philosophy, and build your first preprocessing pipeline. |
| **Cleaning**                               | Learn about cleaning plugins, supported transformations, and configuration options. |
| **Optimization**                           | Understand type inference, memory optimization, and configurable thresholds. |
| **[Analysis](docs/analysis.md)**           | Explore the available analysis plugins, generated reports, and customization options. |
| **[Imputation](docs/imputation.md)**       | Learn about supported imputation strategies and when to use them. |
| **[Configuration](docs/configuration.md)** | Configure cleaning, optimization, analysis, and imputation behavior on a per-DataFrame basis. |
| **Actions**                                | Perform explicit operations such as handling detected outliers after analysis. |
| **Reports**                                | Understand how reports are generated, accessed, and interpreted. |
| **Plugin Development**                     | Create custom plugins and extend `danda` with your own cleaning, optimization, analysis, or imputation logic. |
| **API Reference**                          | Complete reference for the `.dg` accessor, configuration objects, and plugin interfaces. |

### Examples

The `examples/` directory contains complete, runnable examples demonstrating common workflows, including:

- Cleaning raw datasets
- Optimizing memory usage
- Analyzing data quality
- Handling missing values
- Detecting and handling outliers
- Configuring `danda` for different datasets

### Contributing Documentation

Contributions to the documentation are welcome. If you discover missing information, unclear explanations, or opportunities for improvement, please open an issue or submit a pull request.

---

## Roadmap

`danda` is actively evolving to provide a comprehensive toolkit for preparing pandas DataFrames for analysis. The focus remains on **safe**, **deterministic**, and **configurable** data preparation.

see [Roadmap](docs/roadmap.md)

---

# Contributing

Contributions are welcome! Whether you're fixing a bug, improving the documentation, adding a new plugin, or proposing a new feature, your help is appreciated.

see [Contributing](docs/contributing.md)
