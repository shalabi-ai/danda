from collections.abc import Mapping


class ReportRenderer:

    INDENT = "    "

    def render(
            self,
            report: dict,
            hide_redundant: bool = True,
    ) -> str:
        lines = []

        title = "Danda Report"
        lines.append("=" * len(title))
        lines.append(title)
        lines.append("=" * len(title))
        lines.append("")

        for section_name, section in report.items():
            section_lines = self._render_section(
                section_name,
                section,
                hide_redundant,
            )

            if section_lines:
                lines.extend(section_lines)
                lines.append("")

        return "\n".join(lines).rstrip()

    def _render_section(
            self,
            name: str,
            section: Mapping,
            hide_redundant: bool,
    ) -> list[str]:

        content = []

        for key, value in section.items():

            if key == "chain":
                chain = self._render_chain(
                    value,
                    hide_redundant,
                )

                if chain:
                    content.extend(chain)

                continue

            if isinstance(value, Mapping):
                rendered = self._render_mapping(
                    value,
                    hide_redundant,
                )

                if rendered:
                    content.extend(rendered)

            else:
                content.append(str(value))
                content.append("")

        if not content:
            return []

        heading = name.capitalize()

        lines = [
            heading,
            "-" * len(heading),
            "",
            ]

        lines.extend(content)

        return lines

    def _render_mapping(
            self,
            mapping: Mapping,
            hide_redundant: bool,
    ) -> list[str]:

        lines = []

        for name, value in mapping.items():

            if isinstance(value, str):

                if hide_redundant and value.startswith("No "):
                    continue

                lines.append(name)
                lines.append(self._indent_multiline(value))
                lines.append("")

            elif isinstance(value, Mapping):

                nested = self._render_mapping(
                    value,
                    hide_redundant,
                )

                if nested:
                    lines.append(name)
                    lines.extend(nested)
                    lines.append("")

            else:
                lines.append(name)
                lines.append(f"{self.INDENT}{value}")
                lines.append("")

        return lines

    def _render_chain(
            self,
            chain: Mapping,
            hide_redundant: bool,
    ) -> list[str]:

        lines = []

        for _, info in chain.items():

            plugins = info.get("plugin_names", [])
            memory = info.get("memory_usage", {})

            section = [
                "Execution",
                "---------",
                f"Plugins executed : {len(plugins)}",
            ]

            if plugins:
                section.append(
                    f"Plugin names     : {', '.join(plugins)}"
                )

            if memory:
                before = int(memory["before_bytes"])
                after = int(memory["after_bytes"])
                saved = int(memory["saved_bytes"])
                percent = float(memory["saved_percent"])

                if not (hide_redundant and percent < 1.0):
                    section.append(
                        f"Memory before    : {before:,} bytes"
                    )
                    section.append(
                        f"Memory after     : {after:,} bytes"
                    )
                    section.append(
                        f"Memory saved     : {saved:,} bytes ({percent:.1f}%)"
                    )

            lines.extend(section)

        return lines

    def _indent_multiline(self, text: str) -> str:
        return "\n".join(
            self.INDENT + line
            for line in text.splitlines()
        )