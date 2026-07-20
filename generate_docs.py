from pathlib import Path

from danda.plugin_documentation_generator import PluginDocumentationGenerator


def main():
    generator = PluginDocumentationGenerator(
        accessor_file=Path("./src/danda/accessor.py"),
        plugin_root=Path("./src/"),      # repository root
        docs_dir=Path("docs/accessor"),
    )

    generator.generate()
    print("Documentation generated successfully.")


if __name__ == "__main__":
    main()