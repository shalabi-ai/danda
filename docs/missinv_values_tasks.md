# Missing values
My recommendation

If I were prioritizing features for danda, I'd implement them in this order:

1. ✅ NormalizeMissingPlugin (very common and broadly useful)
2. ✅ PotentialMissingValuePlugin (helps users spot dataset-specific placeholders)
3. ✅ DropSparseRowsPlugin
4. ✅ DropSparseColumnsPlugin
5. ⏳ FillMissingValuesPlugin (after profiling and validation features)

This progression fits well with danda's philosophy: first make the data clean and correctly typed, then help users decide how to handle missing information, rather than making potentially destructive assumptions automatically.

---

1. Missing value summary ⭐⭐⭐⭐⭐

Instead of only listing columns with missing values, report overall statistics:

Rows:                 15,000
Columns:                 24

Missing cells:          421 (1.17%)
Columns with missing:     6
Complete rows:        14,102

This gives users an immediate overview.

2. Complete-case report ⭐⭐⭐⭐

Report how many rows contain no missing values.

Complete rows: 93.5%
Incomplete rows: 6.5%

Very common in data quality reports.

3. Rows with many missing values ⭐⭐⭐⭐

Not sparse enough to remove, but worth reporting.

Example:

Rows with >50% missing:
- Row 124
- Row 561
- Row 882

Useful for manual inspection.

4. Missing-value heatmap ⭐⭐⭐

Not as a plugin, but as a visualization:

df.dg.plot_missing()

using matplotlib.

5. Missing-value correlation ⭐⭐⭐

Useful during analysis.

Example:

Salary missing together with Bonus: 96%

This is more exploratory than cleaning, so I'd keep it optional.

6. Consecutive missing values ⭐⭐⭐

For time series:

Temperature

2024-01-01 12
2024-01-02 NaN
2024-01-03 NaN
2024-01-04 NaN
2024-01-05 14

Report:

Temperature contains a run of 3 consecutive missing values.
7. Missing-value percentage thresholds ⭐⭐⭐⭐

Highlight columns exceeding a configurable percentage.

Example:

Columns exceeding 30% missing:

Salary      42%
Address     67%

Often used to decide whether to drop a column.

8. Report constant-value imputations ⭐⭐⭐

When using "constant":

Filled Salary using constant 0.
Filled Country using "Unknown".

More descriptive than just:

Salary: constant (15)
9. Missing-value history ⭐⭐

If several plugins modify missing values, the report could summarize:

Normalized:
24 values

Dropped:
3 empty rows

Imputed:
18 values

This provides a nice end-to-end picture of how missing data was handled.

I would stop here

I would not add things like:

KNN imputation
MICE
Regression imputation
Random Forest imputation
EM algorithm

Those belong in machine learning libraries rather than Danda.



---

## Normalize missing values (highest priority)
Convert all common missing value representations to pd.NA.

Examples:

""          -> <NA>
" "         -> <NA>
"   "       -> <NA>
"NA"        -> <NA>
"N/A"       -> <NA>
"NULL"      -> <NA>
"null"      -> <NA>
"None"      -> <NA>
"none"      -> <NA>
"NaN"       -> <NA>
"nan"       -> <NA>
"-"         -> <NA>
"--"        -> <NA>

Configuration:
```
df.dg.config.missing.normalize_enabled = True

df.dg.config.missing.normalize_values = [
        "",
        "null",
        "none",
        "nan",
        "<na>",
]
df.dg.config.missing.normalize_strip_whitespace=True,
df.dg.config.missing.normalize_ignore_case=True,
```

## Report missing values

No modification, just reporting.

Column      Missing   %
--------------------------
Age           12      2.1%
Salary       421     18.5%
Email          2      0.3%

This should probably be part of profile().

## Drop sparse rows

Example:

Name   Age  Salary
John   NaN   NaN
Mike    20   NaN

Configuration:

missing.drop_sparse_rows = True

missing.row_threshold = 0.8

meaning:

Drop rows with more than 80% missing values.

## Drop sparse columns
Phone
------
NaN
NaN
NaN
123
NaN

Configuration:

missing.drop_sparse_columns = True

missing.column_threshold = 0.95

## Fill missing values 

Probably a separate plugin.

Examples:

numeric -> median
category -> mode
datetime -> forward fill

Configuration:

missing.fill_enabled = False

missing.numeric = "median"
missing.category = "mode"

missing.datetime = "ffill"

## Detect suspicious missing values

Many datasets contain things like

999
9999
-999
UNKNOWN
MISSING
?

These aren't actually nulls.

A plugin could report

Potential missing values

Age:
999 appears 123 times

Status:
UNKNOWN appears 57 times

without automatically converting them.

## Missing value report

This could appear in the report.

MissingValuePlugin

Normalized:
""      -> 123
"NA"    -> 87
"-"     -> 14

Total missing values: 224

## Plugins

Eventually you'd have something like

* NormalizeMissingPlugin
* DropSparseRowsPlugin
* DropSparseColumnsPlugin
* PotentialMissingValuePlugin
* FillMissingValuesPlugin
