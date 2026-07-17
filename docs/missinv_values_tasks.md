# Missing values
My recommendation

If I were prioritizing features for danda, I'd implement them in this order:

1. ✅ NormalizeMissingPlugin (very common and broadly useful)
2. ✅ PotentialMissingValuePlugin (helps users spot dataset-specific placeholders)
3. ✅ DropSparseRowsPlugin
4. ✅ DropSparseColumnsPlugin
5. ⏳ FillMissingValuesPlugin (after profiling and validation features)

This progression fits well with danda's philosophy: first make the data clean and correctly typed, then help users decide how to handle missing information, rather than making potentially destructive assumptions automatically.


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
