# 🚀 Coming Soon

`danda` is just getting started.

Our goal is to make pandas DataFrames **analysis-ready by default**, eliminating repetitive preprocessing code while staying true to the pandas API.

Below are the features planned for future releases.

---

# Data Cleaning

## Normalize missing values

Automatically convert common missing-value representations to `NaN`.

Examples:

```
""
" "
"NA"
"N/A"
"NULL"
"null"
"None"
"-"
```

↓

```python
NaN
```

---

## Standardize text

- Remove leading/trailing whitespace
- Collapse multiple spaces
- Normalize line endings
- Optional lowercase/uppercase conversion

---

## Detect ID columns

Automatically identify columns that should remain strings instead of numbers.

Examples:

- CustomerID
- EmployeeID
- PostalCode
- ZipCode
- PhoneNumber
- ISBN
- ProductCode

---

# Type Optimization

## Integer optimization

Automatically downcast integers.

```
int64
```

↓

```
int8
int16
int32
```

when possible.

---

## Float optimization

Automatically reduce precision where safe.

```
float64
```

↓

```
float32
```

---

## Nullable pandas dtypes

Prefer pandas nullable types.

Examples:

```
int64
```

↓

```
Int64
```

```
bool
```

↓

```
boolean
```

---

## Better datetime detection

Support:

- Unix timestamps
- Timezone-aware datetimes
- Configurable date formats
- Automatic day-first detection

---

# Data Validation

Detect suspicious values before they become bugs.

Examples:

```
Age = -5

Salary = -100

Probability = 1.7

Email = "abc@"

Date = 2050-13-01
```

Generate warnings instead of silently modifying data.

---

# Outlier Detection

Identify unusual observations using statistical methods.

Examples:

- Z-score
- IQR (Interquartile Range)
- Percentile-based detection

Useful for:

- Sales
- Financial data
- Sensor data
- Scientific datasets

---

# Dataset Profiling

Generate a quick overview of a DataFrame.

Example:

```
Rows:              145,321
Columns:           27

Missing values:    2.8%

Duplicate rows:    415

Memory usage:      18.4 MB

Numeric columns:   12
Categorical:        6
Datetime:           3
Boolean:            2
Text:               4
```

---

# Suggestions Engine

Provide recommendations instead of making assumptions.

Examples:

```
CustomerID

Looks like an identifier.

Convert to string?
```

```
Country

Only 5 unique values.

Convert to category?
```

```
Date

95% of values look like dates.

Convert to datetime?
```

---

# Read Functions

Read and automatically clean data in one step.

```python
import danda as dg

df = dg.read_csv("sales.csv")

df = dg.read_excel("sales.xlsx")

df = dg.read_parquet("sales.parquet")
```

---

# Plugin System

Create custom cleaning pipelines.

```python
plugins = [
    dg.EmptyRowsPlugin(),
    dg.EmptyColumnsPlugin(),
    dg.BooleanTypePlugin(),
    dg.DateTimeTypePlugin(),
]

df = dg.read_csv(
    "sales.csv",
    plugins=plugins,
)
```

---

# Configurable Rules

Allow users to customize thresholds.

Examples:

```python
dg.optimize(
    category_threshold=0.10,
    datetime_threshold=0.95,
    numeric_threshold=0.90,
)
```

---

# Reporting

Generate richer reports including:

- Columns modified
- Data types changed
- Rows removed
- Memory saved
- Execution time
- Plugin summary

---

# Performance

Improve scalability for very large datasets.

Goals include:

- Lower memory usage
- Faster type inference
- Vectorized implementations
- Parallel execution where appropriate

---

# Long-Term Vision

We want `danda` to become the **data preparation layer for pandas**.

Instead of writing dozens of preprocessing steps for every project, users should be able to write:

```python
import danda as dg

df = dg.read_csv("sales.csv")

df = (
    df
    .dg.clean()
    .dg.optimize()
)
```

and immediately start exploring or modeling their data.