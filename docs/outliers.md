# Outlier Detection and Treatment

## Overview

Outliers are observations that differ significantly from the rest of the data. They may represent:

- Data entry errors
- Measurement or sensor failures
- Rare but valid observations
- Fraudulent activity
- Natural variation

Outliers can greatly influence statistical analysis, machine learning models, and visualizations. Therefore, identifying and handling them is an essential part of data preprocessing.

---

# Why Outliers Matter

Outliers can:

- Distort the mean and standard deviation
- Reduce model accuracy
- Bias regression coefficients
- Affect clustering algorithms
- Produce misleading visualizations

However, not every outlier should be removed. Some outliers contain valuable information, such as fraudulent transactions or rare medical conditions.

> **Important:** Always understand *why* an outlier exists before deciding how to treat it.

---

# Types of Outliers

## 1. Global Outliers

Values that are far away from all other observations.

Example:

```
Age:
22, 24, 23, 25, 21, 24, 22, 98
```

Here, **98** is clearly different from the rest.

---

## 2. Contextual Outliers

Values that are unusual only under specific conditions.

Example:

```
Temperature (°C)

Summer:
30, 32, 31, 29, 33

Winter:
30
```

A temperature of **30°C** is normal during summer but an outlier during winter.

---

## 3. Collective Outliers

A group of observations that appear normal individually but abnormal together.

Example:

A network monitoring system detects:

```
Request counts:

100
102
98
101
500
520
510
530
```

The cluster of high values may indicate a denial-of-service attack.

---

# Detecting Outliers

There are several techniques available depending on the data distribution and problem.

---

# Method 1: Z-Score

## Concept

The Z-score measures how many standard deviations a value is from the mean.

Formula:

```
Z = (x - μ) / σ
```

Where

- x = observation
- μ = mean
- σ = standard deviation

Typically:

- |Z| > 3 indicates an outlier.

---

## Example

Dataset

```
10, 11, 12, 13, 11, 10, 12, 90
```

### Step 1

Mean

```
μ = 19.875
```

### Step 2

Standard deviation

```
σ ≈ 27.9
```

### Step 3

For value 90

```
Z = (90 − 19.875) / 27.9

≈ 2.51
```

Although 90 looks suspicious, the inflated standard deviation prevents it from exceeding the threshold.

This demonstrates one limitation of the Z-score.

---

## Python Example

```python
from scipy.stats import zscore
import pandas as pd

df["z"] = zscore(df["salary"])

outliers = df[df["z"].abs() > 3]
```

---

# Advantages

- Simple
- Fast
- Works well for normally distributed data

# Limitations

- Sensitive to extreme values
- Assumes approximately normal distribution

---

# Method 2: Interquartile Range (IQR)

The IQR method is one of the most commonly used approaches.

It is robust because it depends on quartiles rather than the mean.

---

## Step 1

Sort the data.

Example

```
5
7
8
9
10
11
12
13
14
15
18
40
```

---

## Step 2

Find quartiles

```
Q1 = 8.5

Q2 = 11.5

Q3 = 14.5
```

---

## Step 3

Calculate IQR

```
IQR = Q3 − Q1

= 14.5 − 8.5

= 6
```

---

## Step 4

Compute boundaries

Lower bound

```
Q1 − 1.5 × IQR

8.5 − 9

= -0.5
```

Upper bound

```
Q3 + 1.5 × IQR

14.5 + 9

= 23.5
```

---

## Step 5

Values outside the interval

```
[-0.5, 23.5]
```

are considered outliers.

Therefore,

```
40
```

is an outlier.

---

## Python Example

```python
Q1 = df["salary"].quantile(0.25)
Q3 = df["salary"].quantile(0.75)

IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

outliers = df[(df["salary"] < lower) | (df["salary"] > upper)]
```

---

# Advantages

- No normality assumption
- Robust to extreme values
- Widely used

# Limitations

- Can label many observations as outliers in skewed distributions

---

# Method 3: Percentile Method

Sometimes observations beyond a chosen percentile are removed.

Example

Remove values below the 1st percentile and above the 99th percentile.

Python

```python
lower = df["salary"].quantile(0.01)
upper = df["salary"].quantile(0.99)

filtered = df[
    (df["salary"] >= lower) &
    (df["salary"] <= upper)
]
```

---

# Method 4: Modified Z-Score

Uses the median instead of the mean.

Formula

```
Modified Z

= 0.6745 × (x − Median)

      ----------------

      Median Absolute Deviation
```

This method is much more robust than the standard Z-score.

---

# Method 5: Isolation Forest

Isolation Forest is an unsupervised machine learning algorithm.

Idea:

- Outliers are easier to isolate than normal observations.

Instead of statistical rules, it randomly partitions data.

Points isolated in fewer splits are considered anomalies.

Python

```python
from sklearn.ensemble import IsolationForest

model = IsolationForest(
    contamination=0.02,
    random_state=42
)

df["outlier"] = model.fit_predict(df[["salary"]])
```

Output

```
1   Normal
-1  Outlier
```

---

# Method 6: Local Outlier Factor (LOF)

LOF compares the density of a point to the density of its neighbors.

If a point has much lower density than surrounding points, it is considered an outlier.

Works well when data contains clusters.

Python

```python
from sklearn.neighbors import LocalOutlierFactor

lof = LocalOutlierFactor()

labels = lof.fit_predict(df[["salary"]])
```

---

# Visual Detection

Visualization often reveals outliers immediately.

---

## Box Plot

```
|------|====|------|
             *
```

The star represents an outlier.

Python

```python
import seaborn as sns

sns.boxplot(data=df["salary"])
```

---

## Scatter Plot

Useful for multidimensional datasets.

```python
import matplotlib.pyplot as plt

plt.scatter(df["age"], df["salary"])
```

Outliers often appear isolated.

---

# How to Handle Outliers

There is no universal solution.

The correct approach depends on why the outlier exists.

---

# Option 1: Remove Outliers

Appropriate when:

- Data entry mistakes
- Sensor failures
- Impossible values

Example

```
Age = 450
```

Clearly invalid.

Python

```python
df = df[
    (df["salary"] >= lower) &
    (df["salary"] <= upper)
]
```

---

# Option 2: Replace with Median

Useful when:

- Outlier is an error
- Dataset is small

Example

```
Before

100
102
101
98
900

Median

101

After

100
102
101
98
101
```

Python

```python
median = df["salary"].median()

df.loc[
    df["salary"] > upper,
    "salary"
] = median
```

---

# Option 3: Winsorization

Instead of removing observations, cap them at specified limits.

Example

Before

```
5
8
9
10
11
200
```

After

```
5
8
9
10
11
15
```

Python

```python
from scipy.stats.mstats import winsorize

df["salary"] = winsorize(
    df["salary"],
    limits=[0.01, 0.01]
)
```

---

# Option 4: Transformation

Apply transformations that reduce skewness.

Examples

- Log transformation
- Square root
- Box-Cox transformation
- Yeo-Johnson transformation

Python

```python
import numpy as np

df["salary"] = np.log1p(df["salary"])
```

---

# Option 5: Keep the Outliers

Sometimes the best decision is to leave them untouched.

Examples

- Fraud detection
- Medical diagnosis
- Rare diseases
- Earthquake prediction
- Financial risk analysis

Removing these observations would remove valuable information.

---

# Complete Example

Suppose we have employee salaries:

| Employee | Salary |
|----------|---------:|
| A | 45,000 |
| B | 48,000 |
| C | 47,500 |
| D | 46,000 |
| E | 49,000 |
| F | 52,000 |
| G | 50,000 |
| H | 350,000 |

### Step 1: Visual Inspection

A box plot immediately reveals that **350,000** is far from the other salaries.

### Step 2: IQR Calculation

- Q1 = 46,750
- Q3 = 50,500
- IQR = 3,750

Upper bound:

```
50,500 + 1.5 × 3,750

= 56,125
```

Since **350,000 > 56,125**, it is classified as an outlier.

### Step 3: Investigate

Before removing the value, ask:

- Is this a data entry mistake?
- Is the employee a CEO?
- Is this a bonus payment?
- Is the salary reported in a different currency?

### Step 4: Decide

Possible actions:

- Remove if it is an error.
- Replace with the median if appropriate.
- Winsorize if modeling requires reduced influence.
- Keep if it represents a legitimate executive salary.

---

# Best Practices

- Never remove outliers automatically.
- Investigate the source of every unusual value.
- Choose a detection method that matches the data distribution.
- Use visualization alongside statistical techniques.
- Document every preprocessing decision.
- Consider the impact on downstream analysis and machine learning models.
- Preserve the original data before making modifications.

---

# Summary

| Method | Best For | Pros | Cons |
|--------|----------|------|------|
| Z-Score | Normally distributed data | Simple and fast | Sensitive to extreme values |
| Modified Z-Score | Skewed data | Robust | Slightly more computation |
| IQR | General-purpose tabular data | Distribution-free and robust | May over-identify outliers in highly skewed data |
| Percentiles | Large datasets | Easy to implement | Thresholds can be arbitrary |
| Isolation Forest | High-dimensional data | Handles complex patterns | Requires parameter tuning |
| Local Outlier Factor | Clustered data | Detects local anomalies | Computationally expensive |
| Visual Inspection | Exploratory analysis | Intuitive and informative | Subjective and not scalable |

---

# Key Takeaways

- Outliers are observations that deviate markedly from the rest of the data.
- They may indicate errors, rare events, or meaningful phenomena.
- Common detection techniques include Z-score, IQR, Modified Z-score, Percentiles, Isolation Forest, and Local Outlier Factor.
- Treatment options include removing, replacing, winsorizing, transforming, or retaining outliers based on the context.
- Effective outlier handling combines statistical methods with domain knowledge to make informed decisions.