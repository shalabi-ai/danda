# clean

Clean a DataFrame using deterministic, low-risk transformations.

The cleaning pipeline performs operations that are considered safe and
objective for almost all datasets. These transformations improve data
consistency without attempting to infer missing information or modify the
semantic meaning of the data.

The following operations are performed:

- Rename columns using the configured naming convention.
- Trim leading and trailing whitespace from string values.
- Normalize common missing-value representations (for example,
  "", "NA", "N/A", "null") to ``pd.NA``.
- Remove sparse columns according to the configured threshold.
- Remove sparse rows according to the configured threshold.
- Remove completely empty rows.
- Remove completely empty columns.
- Remove duplicate rows.

Returns
-------
pandas.DataFrame
    A cleaned copy of the DataFrame.

Notes
-----
A cleaning report is stored in::

    df.attrs["danda_clean_report"]

and can be accessed using::

    df.dg.report["clean"]

Examples
--------
>>> df = pd.read_csv("customers.csv")
>>> df = df.dg.clean()
>>> df.dg.report["clean"]



## RenameColumnsPlugin

Renames DataFrame columns according to the configured naming convention. Supported naming styles are `snake_case`, `camelCase`, and `lowercase`. If multiple columns would result in the same name after conversion, the plugin automatically appends a numeric suffix (for example, `_2`, `_3`) to ensure all column names remain unique.

### Configuration

- rename_column_enabled
- rename_column_style

### Example

input:
pd.DataFrame({
    "First Name": ["Alice", "Bob"],
    "Last-Name": ["Smith", "Jones"],
    "Employee.ID": [101, 102],
    "First_Name": ["A", "B"]
})

Assume the configuration is:
- rename_column_style = ColumnCase.SNAKE

output:
pd.DataFrame({
    "first_name": ["Alice", "Bob"],
    "last_name": ["Smith", "Jones"],
    "employee_id": [101, 102],
    "first_name_2": ["A", "B"]
})

report:
{
    "clean": {
        "RenameColumnsPlugin": {
            "renamed": [
                "employee_id",
                "first_name",
                "first_name_2",
                "last_name"
            ],
            "count": 4
        }
    }
}


## EmptySpacesPlugin

Removes leading and trailing whitespace from all string columns in a pandas DataFrame. Only string columns are processed, while non-string columns remain unchanged. The report lists the columns in which at least one value was modified.

### Configuration

- strip_whitespace

### Example

input:
pd.DataFrame({
    "Name": [" Alice ", "Bob", "  Charlie"],
    "City": [" New York", "London ", " Paris "],
    "Age": [25, 30, 35]
})

output:
pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "City": ["New York", "London", "Paris"],
    "Age": [25, 30, 35]
})

report:
{
    "clean": {
        "EmptySpacesPlugin": ["Name", "City"]
    }
}


## NormalizeMissingValuesPlugin

Normalizes user-defined representations of missing values by replacing matching string values with `pd.NA`. The plugin operates only on string columns and supports optional whitespace trimming and case-insensitive matching before comparing values. Existing missing values are preserved.

### Configuration

- normalize_enabled
- normalize_values
- normalize_strip_whitespace
- normalize_ignore_case

### Example

input:
pd.DataFrame({
    "Name": ["Alice", "N/A", "Bob", " unknown "],
    "City": ["New York", "None", "London", "Paris"],
    "Age": [25, 30, 35, 40]
})

Assume the configuration is:
- normalize_values = ["N/A", "None", "Unknown"]
- normalize_strip_whitespace = True
- normalize_ignore_case = True

output:
pd.DataFrame({
    "Name": ["Alice", pd.NA, "Bob", pd.NA],
    "City": ["New York", pd.NA, "London", "Paris"],
    "Age": [25, 30, 35, 40]
})

report:
{
    "missing": {
        "NormalizeMissingValuesPlugin": {
            "Name": 2,
            "City": 1
        }
    }
}


## SparseColumnsPlugin

Removes columns whose fraction of missing values is greater than or equal to the configured threshold. The missing-value fraction is calculated independently for each column as the number of missing values divided by the total number of rows. Columns with a missing-value fraction below the threshold are retained.

### Configuration

- sparse_columns_enabled
- sparse_columns_threshold

### Example

input:
pd.DataFrame({
    "A": [1, 2, 3, 4],
    "B": [None, None, 3, None],
    "C": [10, 20, 30, 40],
    "D": [None, None, None, None]
})

Assume the configuration is:
- sparse_columns_threshold = 0.75

output:
pd.DataFrame({
    "A": [1, 2, 3, 4],
    "C": [10, 20, 30, 40]
})

report:
{
    "clean": {
        "SparseColumnsPlugin": {
            "columns_removed": 2,
            "columns": ["B", "D"]
        }
    }
}


## SparseRowsPlugin

Removes rows whose fraction of missing values is greater than or equal to the configured threshold. The missing-value fraction is calculated independently for each row as the number of missing values divided by the total number of columns. Rows with a missing-value fraction below the threshold are retained.

### Configuration

- sparse_rows_enabled
- sparse_rows_threshold

### Example

input:
pd.DataFrame({
    "A": [1, None, None, 4],
    "B": [10, None, 30, None],
    "C": [100, None, None, 400],
    "D": [1000, None, 4000, None]
})

Assume the configuration is:
- sparse_rows_threshold = 0.75

output:
pd.DataFrame({
    "A": [1, None, 4],
    "B": [10, 30, None],
    "C": [100, None, 400],
    "D": [1000, 4000, None]
}, index=[0, 2, 3])

report:
{
    "clean": {
        "SparseRowsPlugin": {
            "rows_removed": 1,
            "indices": [1]
        }
    }
}


## EmptyRowsPlugin

Removes rows that contain only missing (`NaN`) values from a pandas DataFrame. A row is removed only if every value in that row is missing. Rows containing at least one non-null value are preserved.

### Configuration

- remove_empty_rows

### Example

input:
pd.DataFrame({
    "A": [1, None, 2, None],
    "B": ["x", None, "y", None]
})

output:
pd.DataFrame({
    "A": [1, 2],
    "B": ["x", "y"]
}, index=[0, 2])

report:
{
    "clean": {
        "EmptyRowsPlugin": 2
    }
}


## EmptyColumnsPlugin

Removes columns that contain only missing (`NaN`) values from a pandas DataFrame. A column is removed only if every value in that column is missing. Columns containing at least one non-null value are preserved.

### Configuration

- remove_empty_columns

### Example

input:
pd.DataFrame({
    "A": [1, 2, 3],
    "B": [None, None, None],
    "C": ["x", None, "z"],
    "D": [None, None, None]
})

output:
pd.DataFrame({
    "A": [1, 2, 3],
    "C": ["x", None, "z"]
})

report:
{
    "clean": {
        "EmptyColumnsPlugin": 2
    }
}


## DropDuplicatesPlugin

Removes duplicate rows from a pandas DataFrame using `pandas.DataFrame.drop_duplicates()`. The plugin preserves the first occurrence of each duplicated row and removes all subsequent duplicates. Optionally, the output DataFrame index can be reset based on the plugin configuration.

### Configuration

- remove_duplicates
- remove_duplicates_ignore_index

### Example

input:
pd.DataFrame({
    "A": [1, 2, 2, 3],
    "B": ["a", "b", "b", "c"],
})

output:
pd.DataFrame({
    "A": [1, 2, 3],
    "B": ["a", "b", "c"],
}, index=[0, 1, 3])

report:
{
    "clean": {
        "DropDuplicates": 1
    }
}
