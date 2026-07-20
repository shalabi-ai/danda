# impute

Impute missing values using the configured imputation strategy.

Missing values are filled according to the configuration defined in
``df.dg.config``. The imputation strategy may vary depending on the
column type and user configuration.

Returns
-------
pandas.DataFrame
    A DataFrame with imputed missing values.

Notes
-----
The imputation behavior is configurable and may use different
strategies for numeric, categorical, boolean, or datetime columns.

An imputation report is stored in::

    df.attrs["danda_impute_report"]

and can be accessed using::

    df.dg.report["impute"]

Examples
--------
>>> df = pd.read_csv("customers.csv")
>>> df = df.dg.impute()
>>> df.dg.report["impute"]



## ImputeMissingValuesPlugin

Imputes missing values according to the data type of each column and the configured imputation strategy. Different strategies can be configured independently for numeric, boolean, categorical, datetime, and text columns. The plugin fills only missing values and leaves all existing values unchanged.

Supported strategies include:
- **Numeric:** `mean`, `median`, `mode`, `constant`
- **Boolean:** `mode`, `constant`
- **Categorical:** `mode`, `constant`
- **Datetime:** `ffill`, `bfill`, `constant`
- **Text:** `mode`, `constant`, `empty`

### Configuration

- enabled
- numeric_strategy
- numeric_constant
- boolean_strategy
- boolean_constant
- category_strategy
- category_constant
- datetime_strategy
- datetime_constant
- text_strategy
- text_constant

### Example

input:
pd.DataFrame({
    "Age": [25, None, 35, 40],
    "IsActive": pd.Series([True, None, True, False], dtype="boolean"),
    "Department": pd.Series(["HR", None, "IT", "HR"], dtype="category"),
    "JoinDate": pd.to_datetime(["2024-01-01", None, "2024-01-03", "2024-01-04"]),
    "City": ["London", None, "Paris", "London"]
})

Assume the configuration is:
- numeric_strategy = "median"
- boolean_strategy = "mode"
- category_strategy = "mode"
- datetime_strategy = "ffill"
- text_strategy = "constant"
- text_constant = "Unknown"

output:
pd.DataFrame({
    "Age": [25.0, 35.0, 35.0, 40.0],
    "IsActive": pd.Series([True, True, True, False], dtype="boolean"),
    "Department": pd.Series(["HR", "HR", "IT", "HR"], dtype="category"),
    "JoinDate": pd.to_datetime([
        "2024-01-01",
        "2024-01-01",
        "2024-01-03",
        "2024-01-04"
    ]),
    "City": ["London", "Unknown", "Paris", "London"]
})

report:
{
    "imputation": {
        "ImputeMissingValuesPlugin": {
            "Age": {
                "strategy": "median",
                "filled": 1
            },
            "IsActive": {
                "strategy": "mode",
                "filled": 1
            },
            "Department": {
                "strategy": "mode",
                "filled": 1
            },
            "JoinDate": {
                "strategy": "ffill",
                "filled": 1
            },
            "City": {
                "strategy": "constant",
                "filled": 1
            }
        }
    }
}
