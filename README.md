# danda
Automatically prepare pandas DataFrames for analysis.
Danda automatically:

* removes empty rows
* removes empty columns
* trims whitespace
* detects dates
* detects booleans
* detects categorical columns
* optimizes memory
* generates a cleaning report


A library that aims to be a drop-in replacement for pd.read_csv() and automatically:

* detects column types
* converts low-cardinality strings to category
* parses dates
* optimizes integer/float dtypes
* trims whitespace
* standardizes missing values ("", "NA", "N/A", "null", etc.)
* removes empty rows and columns
* optionally generates a cleaning report

```
import danda as dg

df = dg.read_csv("sales.csv")
df = dg.read_excel("sales.xlsx")
df = dg.read_parquet("sales.parquet")
```

## Installation

```bash
pip install danda
```

## Usage

```python
import pandas as pd
import danda

df = pd.read_csv("employees.csv")

clean_df = df.dg.clean()
```

## What happens automatically
* Remove empty rows
* Remove empty columns
* Strip whitespace [" John ", " John", "John "] -> John
* Normalize missing values ["", " ", "N/A", "NULL", "None", "-"] -> Nan
* Detect dates 2025-01-01->datetime64[ns]
* Detect booleans [Yes , No , TRUE , FALSE ,0, 1] -> bool
* Detect categorical columns unique values < 20 or unique ratio < 15%
* Optimize integer types int64 -> int8
* Detect IDs: do not do these [CustomerID , ZipCode , PostalCode, Phone]
* Memory optimization: Show users the improvement. Memory before : 95 MB, Memory after  : 21 MB, Reduction     : 77.9%
* Cleaning report: 

## Features
* Validation: WARNING Column Age: 12 invalid values , converted to NaN
* Profiling: Rows 145,000 Columns 24 Missing 3.2% Duplicates 512 Memory 18 MB Categorical 7 Numeric 10 Datetime 3
* suggestions: Suggestions CustomerID Looks like an ID column. Convert to string? [Y/n]
* Plugin system
```
dg.read_csv(
    "sales.csv",
    plugins=[
        dg.TrimWhitespace(),
        dg.ParseDates(),
        dg.RemoveDuplicates(),
        dg.NormalizeMissing(),
    ],
)
```
* Pandas accessor

```
import pandas as pd
import dataforge

df = pd.read_csv("sales.csv")

df.dg.clean()

df.dg.profile()

df.dg.optimize()

df.dg.report()
```

#### Normalize missing values

