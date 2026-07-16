import unittest

from danda.configuration.danda_configuration import DandaConfig


class TestDandaConfig(unittest.TestCase):

    def test_show_contains_all_sections(self):
        config = DandaConfig()

        output = config.show()

        self.assertIn("TypeConfig", output)
        self.assertIn("CleaningConfig", output)

    def test_show_contains_all_settings(self):
        config = DandaConfig()

        output = config.show()

        self.assertIn("category_threshold", output)
        self.assertIn("numeric_threshold", output)
        self.assertIn("remove_duplicates", output)
        self.assertIn("strip_whitespace", output)

    def test_custom_values_are_displayed(self):
        config = DandaConfig()

        config.types.category_threshold = 0.05
        config.cleaning.remove_duplicates = False

        output = config.show()

        self.assertIn("0.05", output)
        self.assertIn("False", output)


if __name__ == '__main__':
    unittest.main()
