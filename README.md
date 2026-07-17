# danda

> **_Stop writing the same pandas preprocessing code over and over._**
> 
> **Automatically clean and optimize pandas DataFrames with one line of code.**

`danda` prepares DataFrames for analysis by performing safe, deterministic cleaning, type inference, and memory optimization while preserving the meaning of the data.

`danda` is a lightweight extension for pandas that prepares messy data for analysis by automatically cleaning, converting data types, and reducing memory usage.

Instead of writing dozens of lines of preprocessing code, simply do:

```python
clean_df = df.dg.clean().dg.optimize()
```

---

## Why danda?

Every data scientist has written code like this:

```python
df = pd.read_csv("sales.csv")

df = df.dropna(how="all")
df = df.dropna(axis=1, how="all")
df = df.drop_duplicates()

df["created_at"] = pd.to_datetime(df["created_at"])
df["active"] = df["active"].astype(bool)
df["country"] = df["country"].astype("category")
df["price"] = pd.to_numeric(df["price"])
```

With **danda**, all of that becomes:

```python
df = pd.read_csv("sales.csv")

df = df.dg.clean().dg.optimize()
```

---

# Features

## 🧹 Data cleaning

Automatically:

- Remove empty rows
- Remove empty columns
- Remove duplicate rows
- Strip leading/trailing whitespace

Example:

| Before | After |
|---------|-------|
| `" John "` | `"John"` |
| `" Alice"` | `"Alice"` |
| `"Bob "` | `"Bob"` |

---

## 📅 Automatic type detection

Automatically converts string columns to their appropriate pandas dtypes.

### Boolean

```
"True"
"False"
"0"
"1"
0
1
```

↓

```
boolean
```

---

### Datetime

```
2024-01-01
2024/01/01
2024-01-01T12:30:00
Jan 1, 2024
```

↓

```
datetime64[ns]
```

---

### Numeric

```
"10"
"25"
"3.14"
```

↓

```
int64 / float64
```

---

### Category

Low-cardinality columns are automatically converted to pandas `category` dtype to reduce memory usage.

Example:

```
Country

Germany
France
Germany
Germany
France
```

↓

```
category
```

---

## 📉 Memory optimization

Optimizing dtypes can dramatically reduce memory usage.

```python
before.dg.compare_memory(after)
```

Example:

```
Before : 95 MB
After  : 21 MB

Saved : 74 MB (77.9%)
```

---

## 📄 Cleaning reports

Every operation produces a report describing what happened.

```python
optimized.dg.report
```

Example:

```python
{
    "clean": {
        "EmptyRowsPlugin":
            "Number of deleted rows: 15",

        "EmptyColumnsPlugin":
            "Number of deleted columns: 2",

        "DropDuplicates":
            "Number of deleted rows: 31"
    },

    "optimize": {
        "BooleanTypePlugin":
            ["active"],

        "DateTimeTypePlugin":
            ["created_at"],

        "NumericTypePlugin":
            ["price"],

        "CategoryTypePlugin":
            ["country"]
    }
}
```

---

## ⚙️ Configuration

`danda` is configurable, allowing you to control how cleaning and type detection behave. Every DataFrame has its own configuration, making it easy to customize behavior for different datasets.

```python
import pandas as pd
import danda

df = pd.read_csv("employees.csv")

# Disable numeric detection
df.dg.config.types.numeric_enabled = False

# Be more strict when detecting categories
df.dg.config.types.category_threshold = 0.05

# Preserve the original index when removing duplicates
df.dg.config.cleaning.remove_duplicates_ignore_index = False

df = df.dg.optimize()
```

You can inspect the current configuration at any time:

```python
print(df.dg.config.show())
```

which produces output similar to:

```text
TypeConfig
==========

Numeric Detection
-----------------

numeric_enabled                    : True
    Default     : True
    Description : Enable automatic detection and conversion of numeric columns.

numeric_threshold                  : 0.95
    Default     : 0.95
    Description : Minimum fraction of non-null values that must be successfully
                  converted to numeric before the column is considered numeric.
```

For a complete list of configuration options and examples, see the
**[Configuration Guide](docs/configuration.md)**.

---

## Filling Missing Values

`danda` can automatically fill missing values after your DataFrame has been cleaned and optimized.

Unlike cleaning operations (such as removing empty rows or converting data types), filling missing values **changes the data**. For this reason, imputation is **disabled by default** and must be explicitly enabled.

#### Supported Strategies

By default, `danda` selects a strategy based on the column data type:

| Data Type | Default Strategy |
| --------- | ---------------- |
| Numeric   | Median           |
| Boolean   | Mode             |
| Category  | Mode             |
| Text      | Mode             |
| Datetime  | Forward fill     |

These strategies can be customized through the configuration.

#### Usage

```python
import danda

df = (
    pd.read_csv("data.csv")
      .dg.clean()
      .dg.optimize()
      .dg.impute()
)
```

Enable imputation:

```python
df.dg.config.imputation.enabled = True
```

Customize strategies:

```python
df.dg.config.imputation.numeric_strategy = "mean"
df.dg.config.imputation.category_strategy = "constant"
df.dg.config.imputation.datetime_strategy = "bfill"
```

#### Report

After imputation, `danda` records which columns were filled and the strategy that was used.

Example:

```text
Filled missing values:
- Age: median (12)
- Salary: mean (4)
- Country: mode (8)
- Date: ffill (2)
```

#### Learn More

For a complete description of the available strategies, configuration options, and implementation details, see **[Imputation Guide](docs/imputation.md)**.

---

## Danda Accessor

Danda extends pandas with the `.dg` accessor, providing a simple and consistent API for cleaning, analyzing, optimizing, and transforming DataFrames.

Instead of calling multiple pandas functions, you can perform common data preparation tasks directly from your DataFrame.

```python
import pandas as pd
import danda

df = pd.read_csv("titanic.csv")

df = (
    df
    .dg.clean()
    .dg.optimize()
    .dg.analyse()
)
```

The accessor groups functionality into logical categories:

| Category | Description |
|----------|-------------|
| **Cleaning** | Remove duplicates, normalize missing values, trim whitespace, remove sparse or empty rows and columns, and other data cleaning operations. |
| **Analysis** | Generate data quality reports, detect missing values, identify suspicious values, find binary columns, and profile dataset quality without modifying the data. |
| **Optimization** | Reduce memory usage by converting data types such as boolean, category, numeric, and datetime where appropriate. |
| **Imputation** | Fill missing values using configurable strategies such as median, mode, forward fill, backward fill, or constant values. |

Each operation preserves the DataFrame interface and can be chained naturally.

```python
df = (
    pd.read_csv("customers.csv")
      .dg.clean()
      .dg.impute_missing_values()
      .dg.optimize()
      .dg.analyse()
)
```

### Reports

Many accessor methods generate detailed reports describing the actions performed or issues detected.

```python
df = df.dg.clean().dg.analyse()

print(df.dg.report())
```

### Learn More

For a complete reference of every accessor method, configuration option, and usage example, see:

- **[Accessor Reference](docs/danda_accessor.md)**

---

# Installation

```bash
pip install danda
```

---

# Quick Start

```python
import pandas as pd
import danda

df = pd.read_csv("employees.csv")

clean = df.dg.clean()

optimized = clean.dg.optimize()

print(optimized.dg.report)

print(clean.dg.compare_memory(optimized))
```

---

# Pandas Accessor

`danda` integrates directly into pandas using a custom accessor.

```python
df.dg.clean()

df.dg.optimize()

df.dg.report

df.dg.compare_memory(other_df)
```

No new DataFrame class.
No wrapper objects.

Just pandas.

---

# Philosophy

`danda` follows a simple principle:

> **Prepare data for analysis automatically while preserving the familiar pandas workflow.**

The library is designed to feel like a natural extension of pandas rather than a replacement.

---

# Roadmap

Planned features include:

- Read functions (`danda.read_csv()`, `read_excel()`, `read_parquet()`)
- Missing value normalization
- Integer downcasting
- Float optimization
- Automatic ID detection
- Data validation
- Dataset profiling
- Configurable plugin pipeline
- Custom plugins

---

# Plugin Architecture

`danda` is built around a plugin system.

Current plugins include:

- EmptyRowsPlugin
- EmptyColumnsPlugin
- DropDuplicatesPlugin
- EmptySpacesPlugin
- BooleanTypePlugin
- DateTimeTypePlugin
- NumericTypePlugin
- CategoryTypePlugin

Creating your own plugins is straightforward, allowing you to customize the cleaning pipeline for your own datasets.

---

# Contributing

Contributions, feature requests, and bug reports are welcome!

If you have an idea that makes data cleaning easier, feel free to open an issue or submit a pull request.

#### Normalize missing values

