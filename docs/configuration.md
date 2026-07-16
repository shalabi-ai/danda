# Configuration

`danda` is designed to work out of the box with sensible defaults, but every cleaning and optimization step can be customized.

Each `DataFrame` has its own configuration object, allowing different datasets to use different settings.

```python
import pandas as pd
import danda

df = pd.read_csv("employees.csv")

# Access the configuration
config = df.dg.config
```

---

# Viewing the Configuration

You can inspect the current configuration at any time.

```python
print(df.dg.config.show())
```

Example output:

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

---

# Cleaning Configuration

Cleaning options control how `df.dg.clean()` behaves.

## Remove Duplicate Rows

Enable or disable duplicate removal.

```python
df.dg.config.cleaning.remove_duplicates = True
```

Default:

```python
True
```

---

## Reset Index After Removing Duplicates

Controls the `ignore_index` argument passed to
`pandas.DataFrame.drop_duplicates()`.

```python
df.dg.config.cleaning.remove_duplicates_ignore_index = True
```

Default:

```python
False
```

---

## Remove Empty Rows

Remove rows where every value is missing.

```python
df.dg.config.cleaning.remove_empty_rows = True
```

Default:

```python
True
```

---

## Remove Empty Columns

Remove columns where every value is missing.

```python
df.dg.config.cleaning.remove_empty_columns = True
```

Default:

```python
True
```

---

## Strip Whitespace

Remove leading and trailing whitespace from string columns.

```python
df.dg.config.cleaning.strip_whitespace = True
```

Default:

```python
True
```

---

# Type Detection Configuration

These options control the behavior of `df.dg.optimize()`.

---

## Boolean Detection

Enable automatic detection of boolean columns.

```python
df.dg.config.types.boolean_enabled = True
```

Default:

```python
True
```

### Detection Threshold

Minimum fraction of non-null values that must be recognized as boolean.

```python
df.dg.config.types.boolean_threshold = 1.0
```

Default:

```python
1.0
```

---

## Potential Boolean Detection

Detect columns that contain exactly two distinct values but are not standard boolean representations.

Examples:

- Male / Female
- Yes / No
- Pass / Fail
- Active / Inactive

```python
df.dg.config.types.potential_boolean_enabled = True
```

Default:

```python
True
```

This plugin reports potential boolean columns but does **not** automatically convert them.

---

## Numeric Detection

Enable automatic numeric conversion.

```python
df.dg.config.types.numeric_enabled = True
```

Default:

```python
True
```

### Detection Threshold

Minimum fraction of non-null values that must successfully convert to numeric.

```python
df.dg.config.types.numeric_threshold = 0.95
```

Default:

```python
0.95
```

---

## Datetime Detection

Enable automatic datetime conversion.

```python
df.dg.config.types.datetime_enabled = True
```

Default:

```python
True
```

### Detection Threshold

Minimum fraction of non-null values that must successfully convert to datetime.

```python
df.dg.config.types.datetime_threshold = 0.95
```

Default:

```python
0.95
```

---

## Category Detection

Enable automatic conversion of low-cardinality columns to the pandas `category` dtype.

```python
df.dg.config.types.category_enabled = True
```

Default:

```python
True
```

### Detection Threshold

Maximum ratio of unique values before a column is considered categorical.

```python
df.dg.config.types.category_threshold = 0.10
```

For example:

| Rows | Unique Values | Ratio | Converted |
|------:|--------------:|------:|:---------:|
| 100 | 5 | 0.05 | ✅ |
| 100 | 10 | 0.10 | ✅ |
| 100 | 20 | 0.20 | ❌ |

Default:

```python
0.10
```

---

# Example

Disable numeric detection and use a stricter category threshold.

```python
import pandas as pd
import danda

df = pd.read_csv("employees.csv")

df.dg.config.types.numeric_enabled = False
df.dg.config.types.category_threshold = 0.05

df = df.dg.optimize()
```

---

# Default Configuration

```python
df.dg.config.show()
```

prints all available configuration options together with their current values, default values, and descriptions.

---

# Future Configuration Options

The configuration system will continue to grow as new features are added.

Planned configuration sections include:

- Missing value normalization
- Numeric dtype optimization (`int64 → int8`)
- Validation rules
- Outlier detection
- ID column detection
- Reading options
- Profiling
- Reporting

