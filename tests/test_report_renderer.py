import unittest

from danda.report_renderer import ReportRenderer


class TestReportRenderer(unittest.TestCase):

    def setUp(self):
        self.renderer = ReportRenderer()

    # ------------------------------------------------------------------
    # _indent_multiline
    # ------------------------------------------------------------------

    def test_indent_multiline_single_line(self):
        text = "Hello"

        expected = "    Hello"

        self.assertEqual(
            self.renderer._indent_multiline(text),
            expected,
        )

    def test_indent_multiline_multiple_lines(self):
        text = "One\nTwo\nThree"

        expected = (
            "    One\n"
            "    Two\n"
            "    Three"
        )

        self.assertEqual(
            self.renderer._indent_multiline(text),
            expected,
        )

    # ------------------------------------------------------------------
    # _render_mapping
    # ------------------------------------------------------------------

    def test_render_mapping_strings(self):
        mapping = {
            "Errors": "Something failed",
            "Warnings": "Be careful",
        }

        result = self.renderer._render_mapping(
            mapping,
            hide_redundant=False,
        )

        self.assertIn("Errors", result)
        self.assertIn("Warnings", result)
        self.assertIn("    Something failed", result)

    def test_render_mapping_hide_redundant(self):
        mapping = {
            "Errors": "No errors found",
            "Warnings": "Something happened",
        }

        result = self.renderer._render_mapping(
            mapping,
            hide_redundant=True,
        )

        self.assertNotIn("Errors", result)
        self.assertIn("Warnings", result)

    def test_render_mapping_nested(self):
        mapping = {
            "Validation": {
                "Errors": "Some error"
            }
        }

        result = self.renderer._render_mapping(
            mapping,
            hide_redundant=False,
        )

        self.assertIn("Validation", result)
        self.assertIn("Errors", result)

    def test_render_mapping_non_string(self):
        mapping = {
            "Count": 10,
            "Enabled": True,
        }

        result = self.renderer._render_mapping(
            mapping,
            hide_redundant=False,
        )

        self.assertIn("Count", result)
        self.assertIn("    10", result)
        self.assertIn("Enabled", result)
        self.assertIn("    True", result)

    # ------------------------------------------------------------------
    # _render_chain
    # ------------------------------------------------------------------

    def test_render_chain_with_memory(self):
        chain = {
            "step1": {
                "plugin_names": ["PluginA", "PluginB"],
                "memory_usage": {
                    "before_bytes": 1000,
                    "after_bytes": 600,
                    "saved_bytes": 400,
                    "saved_percent": 40,
                },
            }
        }

        result = self.renderer._render_chain(
            chain,
            hide_redundant=False,
        )

        text = "\n".join(result)

        self.assertIn("Plugins executed : 2", text)
        self.assertIn("Plugin names     : PluginA, PluginB", text)
        self.assertIn("Memory before", text)
        self.assertIn("Memory saved", text)

    def test_render_chain_hide_small_memory_saving(self):
        chain = {
            "step1": {
                "plugin_names": ["PluginA"],
                "memory_usage": {
                    "before_bytes": 1000,
                    "after_bytes": 995,
                    "saved_bytes": 5,
                    "saved_percent": 0.5,
                },
            }
        }

        result = self.renderer._render_chain(
            chain,
            hide_redundant=True,
        )

        text = "\n".join(result)

        self.assertNotIn("Memory before", text)
        self.assertNotIn("Memory saved", text)

    def test_render_chain_without_plugins(self):
        chain = {
            "step1": {
                "plugin_names": [],
                "memory_usage": {},
            }
        }

        result = self.renderer._render_chain(
            chain,
            hide_redundant=False,
        )

        text = "\n".join(result)

        self.assertIn("Plugins executed : 0", text)
        self.assertNotIn("Plugin names", text)

    # ------------------------------------------------------------------
    # _render_section
    # ------------------------------------------------------------------

    def test_render_section_with_mapping(self):
        section = {
            "summary": {
                "Errors": "None"
            }
        }

        result = self.renderer._render_section(
            "validation",
            section,
            hide_redundant=False,
        )

        self.assertEqual(result[0], "Validation")
        #self.assertIn("summary", result)

    def test_render_section_with_chain(self):
        section = {
            "chain": {
                "step1": {
                    "plugin_names": ["Plugin"],
                    "memory_usage": {},
                }
            }
        }

        result = self.renderer._render_section(
            "execution",
            section,
            hide_redundant=False,
        )

        self.assertIn("Execution", result)

    def test_render_section_plain_values(self):
        section = {
            "message": "Everything OK"
        }

        result = self.renderer._render_section(
            "status",
            section,
            hide_redundant=False,
        )

        self.assertIn("Everything OK", result)

    def test_render_section_empty(self):
        result = self.renderer._render_section(
            "empty",
            {},
            hide_redundant=False,
        )

        self.assertEqual(result, [])

    # ------------------------------------------------------------------
    # render()
    # ------------------------------------------------------------------

    def test_render_empty_report(self):
        report = {}

        output = self.renderer.render(report)

        self.assertIn("Danda Report", output)

    def test_render_complete_report(self):
        report = {
            "validation": {
                "summary": {
                    "Errors": "None"
                }
            },
            "execution": {
                "chain": {
                    "step1": {
                        "plugin_names": [
                            "PluginA",
                            "PluginB",
                        ],
                        "memory_usage": {
                            "before_bytes": 100,
                            "after_bytes": 80,
                            "saved_bytes": 20,
                            "saved_percent": 20,
                        },
                    }
                }
            },
        }

        output = self.renderer.render(report)

        self.assertIn("Danda Report", output)
        self.assertIn("Validation", output)
        self.assertIn("Execution", output)
        self.assertIn("PluginA", output)
        self.assertIn("Memory saved", output)

    def test_render_hides_redundant_messages(self):
        report = {
            "validation": {
                "summary": {
                    "Errors": "No errors found"
                }
            }
        }

        output = self.renderer.render(
            report,
            hide_redundant=True,
        )

        self.assertNotIn("No errors found", output)


if __name__ == "__main__":
    unittest.main()

