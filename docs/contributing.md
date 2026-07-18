## Contributing

Contributions are welcome! Whether you're fixing a bug, improving the documentation, adding a new plugin, or proposing a new feature, your help is appreciated.
see [Contributing](docs/contributing.md)

### Ways to Contribute

You can contribute by:

- Reporting bugs
- Suggesting new features
- Improving documentation
- Adding unit tests
- Optimizing existing plugins
- Implementing new cleaning, optimization, analysis, or imputation plugins
- Improving performance
- Reviewing pull requests

If you're unsure where to start, browse the open issues or start a discussion with your idea.

---

### Development Principles

`danda` follows a few core principles that should guide all contributions.

#### Keep it Safe

Automatic transformations should have a very low risk of changing the meaning of the data.

Good examples include:

- Removing completely empty rows
- Trimming whitespace
- Detecting data types

Poor examples include:

- Removing outliers automatically
- Filling missing values automatically
- Scaling numeric values

These operations require user intent and should be implemented as explicit actions or configurable features.

---

#### Keep it Objective

Plugins should perform operations that have little ambiguity.

If two reasonable users could disagree about the correct transformation, it probably should not happen automatically.

---

#### Keep Plugins Focused

Each plugin should have a single responsibility.

For example:

- Detect outliers
- Report missing values
- Remove duplicate rows
- Convert numeric columns

Avoid combining multiple unrelated tasks into a single plugin.

---

#### Make Everything Configurable

Behavior that may vary between datasets should be configurable through the appropriate configuration section.

Avoid hardcoding thresholds, limits, or detection rules.

---

#### Test Everything

New features should include comprehensive unit tests.

Tests should verify:

- Correct behavior
- Edge cases
- Empty DataFrames
- Missing values
- Configuration options
- Generated reports

`danda` uses Python's built-in `unittest` framework.

---

### Plugin Development

New functionality should generally be implemented as a plugin rather than modifying existing plugins.

Depending on the feature, create a:

- Cleaning plugin
- Optimization plugin
- Analysis plugin
- Imputation plugin

This keeps the architecture modular, reusable, and easy to maintain.

---

### Coding Style

Please follow the existing project style:

- Use type hints.
- Write clear, descriptive docstrings.
- Prefer small, focused classes.
- Keep plugins independent.
- Write readable, maintainable code.
- Add tests for all new functionality.

---

### Pull Requests

Before submitting a pull request, please ensure that:

- All tests pass.
- New functionality includes unit tests.
- Documentation has been updated where appropriate.
- Public APIs are documented.
- Code follows the project's style and architecture.

---

Thank you for helping make **danda** better! Every contribution—whether it's code, documentation, bug reports, or feature ideas—helps improve the project for the entire community.
