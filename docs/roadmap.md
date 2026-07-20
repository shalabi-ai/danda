## Roadmap

`danda` is actively evolving to provide a comprehensive toolkit for preparing pandas DataFrames for analysis. The focus remains on **safe**, **deterministic**, and **configurable** data preparation.

see [Roadmap](docs/roadmap.md)

### Planned Features

#### 📊 Additional Analysis Plugins

Expand the collection of data quality reports, including:

- Impossible value detection
- Duplicate value analysis
- High cardinality reports
- Low variance detection
- Correlation analysis
- Identifier and key analysis
- Text column profiling
- Data distribution summaries

---

#### 🧹 Additional Cleaning Plugins

Introduce additional safe cleaning operations, such as:

- Consistent string normalization
- Unicode normalization
- Invisible character removal
- Column name normalization
- Duplicate column detection

---

#### ⚡ Enhanced Type Optimization

Improve automatic type inference with support for:

- Nullable pandas data types
- Currency detection
- Percentage detection
- Time-only columns
- Timedelta detection

---

#### 🩹 Expanded Imputation

Support additional missing value strategies, including:

- Group-based imputation
- Interpolation
- Random sampling
- Custom user-defined strategies

---

#### 🎯 More Actions

Extend the Actions API with explicit data manipulation operations based on analysis results.

Examples include:

- Handle missing values
- Remove constant columns
- Remove duplicate rows
- Handle impossible values
- Handle suspicious missing values

Actions will remain **explicit** and will never be performed automatically.

---

#### 🔌 Plugin Ecosystem

Continue improving the plugin architecture by making it easier to:

- Develop custom plugins
- Share reusable plugins
- Package third-party plugin collections
- Extend reports and configuration

---

#### 📚 Documentation and Examples

Expand the documentation with:

- End-to-end tutorials
- Real-world datasets
- Best practices
- Performance benchmarks
- Plugin development guides

---

## Long-Term Vision

The goal of `danda` is to become the standard first step after loading a pandas DataFrame.

```python
df = (
    pd.read_csv("data.csv")
      .dg.clean()
      .dg.optimize()
      .dg.analyze()
)
```

By providing safe defaults, transparent reporting, and a flexible plugin architecture, `danda` aims to eliminate repetitive preprocessing code while giving users complete control over how their data is prepared.
