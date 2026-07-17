Load DataFrame
│
▼
clean()
│
├── Normalize null values
└
│
▼
optimize()
│
└── Downcast numerics
│
▼
validate()
│
├── Mixed types
├── Remaining object columns
├── Missing values
├── Duplicate column names
└── Warnings
│
analyze()
│
├── PotentialDateTimeTypePlugin
├── PotentialCategoryTypePlugin
├── PotentialNumericTypePlugin
├── MixedTypesPlugin
├── ConstantColumnsPlugin
│
▼
Report