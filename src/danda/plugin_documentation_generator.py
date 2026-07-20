from __future__ import annotations

import ast
import re
from pathlib import Path


class PluginDocumentationGenerator:
    """
    Reads accessor.py, extracts plugin pipelines from accessor methods,
    reads the plugin docstrings from the plugin source files, and generates
    one markdown file per accessor function.

    Output:
        docs/<function_name>.md
    """

    def __init__(
        self,
        accessor_file: str | Path,
        plugin_root: str | Path,
        docs_dir: str | Path = "docs",
    ):
        self.accessor_file = Path(accessor_file)
        self.plugin_root = Path(plugin_root)
        self.docs_dir = Path(docs_dir)

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #

    def generate(self):
        self.docs_dir.mkdir(parents=True, exist_ok=True)

        accessor_tree = ast.parse(self.accessor_file.read_text())

        imports = self._extract_imports(accessor_tree)

        for node in accessor_tree.body:
            if isinstance(node, ast.ClassDef):
                self._process_class(node, imports)

    # ------------------------------------------------------------------ #
    # Accessor parsing
    # ------------------------------------------------------------------ #

    def _process_class(self, cls: ast.ClassDef, imports: dict[str, str]):

        for fn in cls.body:
            if not isinstance(fn, ast.FunctionDef):
                continue

            plugins = self._extract_plugins(fn)

            if not plugins:
                continue

            #doc = ast.get_docstring(node)
            markdown = []
            markdown.append(f"# {fn.name}")
           # markdown.append("")
            markdown.append(self._extract_function_doc(fn, fn.name))
            markdown.append("")

            for plugin in plugins:

                full_name = imports.get(plugin)

                if full_name is None:
                    continue

                source = self._find_plugin_source(full_name)

                if source is None:
                    continue

                info = self._extract_plugin_doc(source, plugin)

                if info is None:
                    continue

                markdown.append(info)

            if markdown:
                output = self.docs_dir / f"{fn.name}.md"
                output.write_text("\n\n".join(markdown), encoding="utf8")

    # ------------------------------------------------------------------ #
    # Import extraction
    # ------------------------------------------------------------------ #

    def _extract_imports(self, tree: ast.AST) -> dict[str, str]:
        """
        Returns

            {
                "DropDuplicatesPlugin":
                    "danda.plugins.clean.drop_duplicates.DropDuplicatesPlugin"
            }
        """

        result = {}

        for node in tree.body:

            if isinstance(node, ast.ImportFrom):

                module = node.module

                for alias in node.names:
                    result[alias.asname or alias.name] = (
                        f"{module}.{alias.name}"
                    )

        return result

    def _extract_function_doc(
        self,
        fn: ast.FunctionDef,
        function_name: str,
    ) -> str | None:
        for node in ast.walk(fn):
            doc = ast.get_docstring(node)
            return doc
            #if isinstance(node, ast.ClassDef) and node.name == function_name:

             #   return ast.get_docstring(node)

        return None
    # ------------------------------------------------------------------ #
    # Plugin list extraction
    # ------------------------------------------------------------------ #

    def _extract_plugins(self, fn: ast.FunctionDef) -> list[str]:
        """
        Looks for

        plugins = [
            PluginA(...),
            PluginB(...),
        ]
        """

        plugins = []

        for node in ast.walk(fn):

            if not isinstance(node, ast.Assign):
                continue

            for target in node.targets:

                if (
                    isinstance(target, ast.Name)
                    and target.id == "plugins"
                    and isinstance(node.value, ast.List)
                ):

                    for item in node.value.elts:

                        if isinstance(item, ast.Call):

                            if isinstance(item.func, ast.Name):
                                plugins.append(item.func.id)

                            elif isinstance(item.func, ast.Attribute):
                                plugins.append(item.func.attr)

        return plugins

    # ------------------------------------------------------------------ #
    # Plugin file lookup
    # ------------------------------------------------------------------ #

    def _find_plugin_source(self, dotted_name: str) -> Path | None:

        module = ".".join(dotted_name.split(".")[:-1])

        relative = Path(*module.split(".")).with_suffix(".py")

        candidate = self.plugin_root / relative

        if candidate.exists():
            return candidate

        return None

    # ------------------------------------------------------------------ #
    # Extract plugin documentation
    # ------------------------------------------------------------------ #

    def _extract_plugin_doc(
        self,
        source_file: Path,
        class_name: str,
    ) -> str | None:

        text = source_file.read_text(encoding="utf8")

        tree = ast.parse(text)

        for node in tree.body:

            if isinstance(node, ast.ClassDef) and node.name == class_name:

                doc = ast.get_docstring(node)

                if not doc:
                    return None

                return self._convert_doc(class_name, doc)

        return None



    # ------------------------------------------------------------------ #
    # Convert plugin documentation into markdown
    # ------------------------------------------------------------------ #

    def _convert_doc(self, class_name: str, doc: str) -> str:

        description = ""
        configuration = ""
        example = ""

        m = re.search(
            r"^(.*?)Plugin Configuration:",
            doc,
            flags=re.S,
        )

        if m:
            description = m.group(1).strip()

        m = re.search(
            r"Plugin Configuration:(.*?)Example:",
            doc,
            flags=re.S,
        )

        if m:
            configuration = m.group(1).strip()

        m = re.search(
            r"Example:(.*)",
            doc,
            flags=re.S,
        )

        if m:
            example = m.group(1).strip()

        return f"""## {class_name}

{description}

### Configuration

{configuration}

### Example

{example}
"""

    def _title_from_doc(self, doc: str) -> str:
        """
        Uses the first sentence as the section title if no better title exists.
        """
        first = doc.strip().split("\n")[0]
        return first.rstrip(".")


def main():
    generator = PluginDocumentationGenerator(
        accessor_file=Path("danda/accessor.py"),
        plugin_root=Path("."),      # repository root
        docs_dir=Path("docs"),
    )

    generator.generate()
    print("Documentation generated successfully.")


if __name__ == "__main__":
    main()