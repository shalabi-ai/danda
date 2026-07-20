# Sample Datasets for Testing Danda

The following public datasets are excellent for testing Danda's cleaning, analysis, optimization, and imputation features.

| Dataset | Description | Best For |
|----------|-------------|----------|
| **Titanic** | Passenger survival dataset with missing ages, cabins, and categorical values. | Missing values, imputation, type inference |
| https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv | | |
| **Iris** | Classic machine learning dataset with numeric features and a categorical target. | Type optimization, profiling |
| https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv | | |
| **Tips** | Restaurant tips dataset. | Numeric optimization, categorical detection |
| https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv | | |
| **Penguins** | Palmer Penguins dataset containing missing values and mixed data types. | Missing value analysis, type inference |
| https://raw.githubusercontent.com/mwaskom/seaborn-data/master/penguins.csv | | |
| **Diamonds** | Large dataset with numeric and categorical columns. | Memory optimization, profiling |
| https://raw.githubusercontent.com/mwaskom/seaborn-data/master/diamonds.csv | | |
| **Titanic (Seaborn)** | Alternative Titanic dataset. | Cleaning examples |
| https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv | | |
| **Flights** | Monthly airline passenger counts. | Datetime handling, time series |
| https://raw.githubusercontent.com/mwaskom/seaborn-data/master/flights.csv | | |
| **Exercise** | Exercise experiment dataset with categorical and datetime information. | Mixed data types |
| https://raw.githubusercontent.com/mwaskom/seaborn-data/master/exercise.csv | | |
| **Planets** | Exoplanet discoveries with many missing values. | Missing value reporting and imputation |
| https://raw.githubusercontent.com/mwaskom/seaborn-data/master/planets.csv | | |

---

# Large CSV Datasets

For benchmarking and stress testing.

## Datablist Sample CSV Files

https://github.com/datablist/sample-csv-files

Provides datasets ranging from **100 rows** to **2 million rows**, including:

- Customers
- Organizations
- Products
- Users

Ideal for testing:

- Memory optimization
- Performance
- Large-file support

---

# Real-World Dataset Collections

## MOSTLY AI Public Demo Data

https://github.com/mostly-ai/public-demo-data

Contains datasets such as:

- Airbnb
- Airlines
- Netflix
- Taxi Trips
- Online Shopping
- Banking
- Healthcare

Useful for testing Danda on realistic datasets.

---

# Recommended Datasets for Documentation

These datasets provide good coverage of Danda's capabilities.

| Dataset | Demonstrates |
|----------|--------------|
| Titanic | Cleaning, missing values, imputation, optimization |
| Penguins | Missing values, type inference |
| Planets | Missing value reporting and sparse data |
| Diamonds | Memory optimization |
| Flights | Datetime handling and imputation |
| Iris | Type optimization |
| Tips | Category detection and numeric optimization |

These datasets are all publicly available and can be loaded directly with:

```python
import pandas as pd

df = pd.read_csv("<dataset-url>")
```