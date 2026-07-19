🎯 Priority 1 — Data profiling (highest value)

These plugins provide immediate insight into a dataset.

Duplicate Summary Plugin

Instead of just deleting duplicates, report them.

Duplicate Summary

Duplicate rows: 42 (1.2%)
Unique rows: 3,481
Column Summary Plugin

A compact overview.

Column Summary

Age
Type: float64
Missing: 177
Unique: 88

Sex
Type: category
Missing: 0
Unique: 2
Constant Columns Plugin

Find columns with only one value.

Constant columns detected:

- Country
- Currency

These are often candidates for removal.

High Cardinality Plugin

Useful before converting to category.

High-cardinality columns:

CustomerID
Email
TransactionID
Unique Identifier Detection

Identify columns that are probably IDs.

Potential identifier columns:

PassengerId
OrderID
UUID

🎯 Priority 2 — Validation

Move from "cleaning" into "data quality."

Outlier Report

Numeric columns.

Age

Outliers: 14

Range:
-5
110

Configurable via IQR or Z-score.

Invalid Date Report

Values that failed datetime parsing.

Invalid Numeric Report

Examples:

"12a"
"$45"
"??"

Useful before type conversion.

Mixed Type Detection
Salary

Types detected:

- int
- str

One of my favorite analysis plugins because mixed-type columns are a common source of bugs.

🎯 Priority 3 — Cleaning
Trim Internal Whitespace
John    Smith

↓

John Smith
Normalize Case
USA
usa
Usa

↓

USA

Configurable.

Rename Columns
snake_case

camelCase

lower

This is something users almost always end up doing.

Remove Constant Columns

Complementary to the analysis plugin.

🎯 Priority 4 — Optimization
Integer Downcasting
int64

↓

int8

Memory savings can be substantial.

Float Downcasting
float64

↓

float32
String Backend

Convert object strings to pandas' nullable string dtype.

🎯 Priority 5 — Reporting

You're already heading in this direction.

I'd add:

Markdown Report
df.dg.report(format="markdown")
HTML Report
df.dg.report(format="html")
JSON Report
df.dg.report(format="json")

These make it easy to integrate Danda into notebooks, CI pipelines, or documentation.

🎯 Priority 6 — Pipeline usability
Dry Run
df.dg.clean(dry_run=True)

Shows what would happen without modifying the DataFrame.

Plugin Timing
NormalizeMissingValuesPlugin

2.4 ms

CategoryPlugin

11.8 ms

Very useful for performance tuning.

Pipeline Summary
Cleaning
---------
Rows removed: 18

Columns removed: 2

Duplicates removed: 7

Optimization
------------
Memory saved: 38%

Analysis
--------
Issues found: 5
Features I'd postpone

These are valuable but can wait until Danda's core is fully established:

Schema validation
Automatic feature engineering
Machine-learning-based imputers
Parallel execution
Great Expectations integration
Spark support
Polars backend
SQL connectors
What I'd target for the next release

A focused release could include:

✅ Complete report renderer (Markdown, HTML, JSON)
✅ Duplicate Summary Plugin
✅ Constant Columns Plugin
✅ High Cardinality Plugin
✅ Unique Identifier Detection Plugin
✅ Mixed Type Detection Plugin
✅ Integer and float downcasting
✅ Column Summary Plugin

That would make Danda feel like a complete data quality and optimization toolkit while staying true to its current design philosophy.