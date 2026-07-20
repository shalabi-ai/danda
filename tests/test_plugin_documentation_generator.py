import ast
import tempfile
import unittest
from pathlib import Path

from danda.plugin_documentation_generator import PluginDocumentationGenerator


class TestPluginDocumentationGenerator(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

        self.accessor = self.root / "accessor.py"
        self.plugin_root = self.root
        self.docs_dir = self.root / "docs"

        self.generator = PluginDocumentationGenerator(
            accessor_file=self.accessor,
            plugin_root=self.plugin_root,
            docs_dir=self.docs_dir,
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_extract_imports(self):
        source = """
from package.plugins import PluginA
from another.module import PluginB as AliasPlugin
"""

        tree = ast.parse(source)

        imports = self.generator._extract_imports(tree)

        expected = {
            "PluginA": "package.plugins.PluginA",
            "AliasPlugin": "another.module.PluginB",
        }

        self.assertEqual(imports, expected)

    def test_extract_plugins(self):
        source = """
def fn():
    plugins = [
        PluginA(),
        PluginB(x=1),
        module.PluginC(),
    ]
"""

        fn = ast.parse(source).body[0]

        plugins = self.generator._extract_plugins(fn)

        self.assertEqual(
            plugins,
            ["PluginA", "PluginB", "PluginC"],
        )

    def test_extract_plugins_empty(self):
        source = """
def fn():
    x = []
"""

        fn = ast.parse(source).body[0]

        self.assertEqual(
            self.generator._extract_plugins(fn),
            [],
        )

    def test_find_plugin_source_exists(self):
        plugin = self.root / "pkg" / "plugins.py"
        plugin.parent.mkdir(parents=True)
        plugin.write_text("")

        path = self.generator._find_plugin_source(
            "pkg.plugins.PluginA"
        )

        self.assertEqual(path, plugin)

    def test_find_plugin_source_missing(self):
        path = self.generator._find_plugin_source(
            "missing.plugins.PluginA"
        )

        self.assertIsNone(path)

    def test_extract_plugin_doc(self):
        plugin = self.root / "plugin.py"

        plugin.write_text(
            '''
class PluginA:
    """
Description

Plugin Configuration:
param: value

Example:
PluginA()
    """
''',
            encoding="utf8",
        )

        result = self.generator._extract_plugin_doc(
            plugin,
            "PluginA",
        )

        self.assertIn("## PluginA", result)
        self.assertIn("Description", result)
        self.assertIn("Configuration", result)
        self.assertIn("Example", result)

    def test_extract_plugin_doc_missing_docstring(self):
        plugin = self.root / "plugin.py"

        plugin.write_text(
            """
class PluginA:
    pass
""",
            encoding="utf8",
        )

        result = self.generator._extract_plugin_doc(
            plugin,
            "PluginA",
        )

        self.assertIsNone(result)

    def test_extract_plugin_doc_missing_class(self):
        plugin = self.root / "plugin.py"

        plugin.write_text(
            """
class AnotherPlugin:
    \"""Doc\"""
""",
            encoding="utf8",
        )

        result = self.generator._extract_plugin_doc(
            plugin,
            "PluginA",
        )

        self.assertIsNone(result)

    def test_convert_doc(self):
        doc = """
This plugin removes duplicates.

Plugin Configuration:
columns: list[str]

Example:
PluginA(columns=["id"])
"""

        md = self.generator._convert_doc(
            "PluginA",
            doc,
        )

        self.assertIn("## PluginA", md)
        self.assertIn("This plugin removes duplicates.", md)
        self.assertIn("columns: list[str]", md)
        self.assertIn('PluginA(columns=["id"])', md)

    def test_title_from_doc(self):
        title = self.generator._title_from_doc(
            "First sentence.\nSecond line."
        )

        self.assertEqual(title, "First sentence")

    def test_extract_function_doc(self):
        source = '''
def fn():
    """Function documentation."""
    pass
'''

        fn = ast.parse(source).body[0]

        doc = self.generator._extract_function_doc(
            fn,
            "fn",
        )

        self.assertEqual(doc, "Function documentation.")

    def test_generate_creates_markdown(self):
        self.accessor.write_text(
            """
from plugins.sample import SamplePlugin

class Accessor:

    def clean(self):
        \"""Clean data.\"""

        plugins = [
            SamplePlugin(),
        ]
""",
            encoding="utf8",
        )

        plugin_dir = self.root / "plugins"
        plugin_dir.mkdir()

        (plugin_dir / "sample.py").write_text(
            '''
class SamplePlugin:
    """
Sample plugin.

Plugin Configuration:
value: int

Example:
SamplePlugin()
    """
''',
            encoding="utf8",
        )

        self.generator.generate()

        output = self.docs_dir / "clean.md"

        self.assertTrue(output.exists())

        content = output.read_text()

        self.assertIn("# clean", content)
        self.assertIn("Sample plugin.", content)
        self.assertIn("Configuration", content)
        self.assertIn("Example", content)

    def test_generate_skips_missing_plugin(self):
        self.accessor.write_text(
            """
from plugins.sample import SamplePlugin

class Accessor:

    def clean(self):
        plugins = [
            SamplePlugin(),
        ]
""",
            encoding="utf8",
        )

        self.generator.generate()

        output = self.docs_dir / "clean.md"

        self.assertTrue(output.exists())


if __name__ == "__main__":
    unittest.main()
