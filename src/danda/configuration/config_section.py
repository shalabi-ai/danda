from dataclasses import fields
from collections import defaultdict
import textwrap

class ConfigSection:

    def show(self) -> str:
        """
        Return a human-readable representation of the configuration grouped
        by feature.
        """
        groups = defaultdict(list)

        # Group fields by feature
        for f in fields(self):
            feature = f.metadata.get("feature", "General")
            groups[feature].append(f)

        lines = [
            self.__class__.__name__,
            "=" * len(self.__class__.__name__),
            "",
            ]

        for feature, feature_fields in groups.items():
            title = feature.replace("_", " ").title()

            lines.append(title)
            lines.append("-" * len(title))
            lines.append("")

            for f in feature_fields:
                value = getattr(self, f.name)
                default = f.default
                description = f.metadata.get("description", "")

                lines.append(f"{f.name:<35}: {value}")
                lines.append(f"    {'Default':<12}: {default}")

                if description:
                    wrapped = textwrap.fill(
                        description,
                        width=88,
                        initial_indent=f"    {'Description':<12}: ",
                        subsequent_indent=" " * 18,
                    )
                    lines.append(wrapped)

                lines.append("")

        return "\n".join(lines)

    def __repr__(self):
        return self.show()