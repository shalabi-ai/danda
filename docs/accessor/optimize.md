# optimize

Optimize column data types for analysis and memory efficiency.

The optimization pipeline automatically detects appropriate pandas
dtypes and converts columns when the conversion is considered safe.

The following conversions are performed:

- Convert boolean-like values to boolean dtype.
- Convert datetime-like values to datetime dtype.
- Convert numeric strings to numeric dtypes.
- Convert low-cardinality object columns to categorical dtype.

Returns
-------
pandas.DataFrame
    A DataFrame with optimized column dtypes.

Notes
-----
Existing values are preserved whenever possible. Columns are converted
only when they satisfy the configured detection thresholds.

An optimization report is stored in::

    df.attrs["danda_optimize_report"]

and can be accessed using::

    df.dg.report["optimize"]

Examples
--------
>>> df = pd.read_csv("sales.csv")
>>> df = df.dg.optimize()
>>> df.dtypes



## BooleanTypePlugin

Converts columns identified as containing boolean values to pandas' nullable `boolean` data type. Supported boolean representations include `True`, `False`, `"true"`, `"false"`, `"1"`, `"0"`, `1`, and `0`. String values are matched case-insensitively before conversion, and missing values are preserved.

### Configuration

- boolean_enabled

### Example

input:
pd.DataFrame({
    "IsActive": ["True", "false", "1", "0", None],
    "Verified": [1, 0, 1, 0, None],
    "Name": ["Alice", "Bob", "Charlie", "David", "Eve"]
})

output:
pd.DataFrame({
    "IsActive": [True, False, True, False, pd.NA],
    "Verified": [True, False, True, False, pd.NA],
    "Name": ["Alice", "Bob", "Charlie", "David", "Eve"]
}).astype({
    "IsActive": "boolean",
    "Verified": "boolean"
})

report:
{
    "types": {
        "BooleanTypePlugin": [
            "IsActive",
            "Verified"
        ]
    }
}


## DateTimeTypePlugin

Converts string columns that predominantly contain date or datetime values to the pandas `datetime64[ns]` data type. A column is converted when the fraction of successfully parsed non-missing values is greater than or equal to the configured threshold. Values that cannot be parsed are converted to `NaT`.

### Configuration

- datetime_enabled
- datetime_threshold

### Example

input:
pd.DataFrame({
    "OrderDate": ["2024-01-01", "2024-02-15", "2024-03-20", None],
    "ShipDate": ["01/05/2024", "2024-02-18", "March 25, 2024", "invalid"],
    "Customer": ["Alice", "Bob", "Charlie", "David"]
})

Assume the configuration is:
- datetime_threshold = 0.75

output:
pd.DataFrame({
    "OrderDate": [
        pd.Timestamp("2024-01-01"),
        pd.Timestamp("2024-02-15"),
        pd.Timestamp("2024-03-20"),
        pd.NaT
    ],
    "ShipDate": [
        pd.Timestamp("2024-01-05"),
        pd.Timestamp("2024-02-18"),
        pd.Timestamp("2024-03-25"),
        pd.NaT
    ],
    "Customer": ["Alice", "Bob", "Charlie", "David"]
})

report:
{
    "types": {
        "DateTimeTypePlugin": [
            "OrderDate",
            "ShipDate"
        ]
    }
}


## NumericTypePlugin

Converts string columns containing numeric values to a pandas numeric data type (`int64` or `float64`, depending on the data). A column is converted when the fraction of successfully parsed non-missing values is greater than or equal to the configured threshold. Values that cannot be parsed are converted to `NaN`.

### Configuration

- numeric_enabled
- numeric_threshold

### Example

input:
pd.DataFrame({
    "Age": ["25", "30", "35", None],
    "Salary": ["50000.5", "62000", "71000.25", "80000"],
    "Name": ["Alice", "Bob", "Charlie", "David"]
})

Assume the configuration is:
- numeric_threshold = 1.0

output:
pd.DataFrame({
    "Age": [25.0, 30.0, 35.0, pd.NA],
    "Salary": [50000.5, 62000.0, 71000.25, 80000.0],
    "Name": ["Alice", "Bob", "Charlie", "David"]
})

report:
{
    "types": {
        "NumericTypePlugin": [
            "Age",
            "Salary"
        ]
    }
}


## CategoryTypePlugin

Converts low-cardinality, non-numeric columns to the pandas `category` data type. A column is considered categorical when the ratio of unique non-missing values to the total number of rows is less than or equal to the configured threshold. Columns that are already boolean, datetime, categorical, or fully numeric are excluded.

### Configuration

- category_enabled
- category_threshold

### Example

input:
pd.DataFrame({
    "Color": ["Red", "Blue", "Red", "Blue", "Red"],
    "Department": ["HR", "IT", "HR", "IT", "HR"],
    "Name": ["Alice", "Bob", "Charlie", "David", "Eve"],
    "Age": [25, 30, 35, 40, 45]
})

Assume the configuration is:
- category_threshold = 0.5

output:
pd.DataFrame({
    "Color": ["Red", "Blue", "Red", "Blue", "Red"],
    "Department": ["HR", "IT", "HR", "IT", "HR"],
    "Name": ["Alice", "Bob", "Charlie", "David", "Eve"],
    "Age": [25, 30, 35, 40, 45]
}).astype({
    "Color": "category",
    "Department": "category"
})

report:
{
    "types": {
        "CategoryTypePlugin": [
            "Color",
            "Department"
        ]
    }
}
