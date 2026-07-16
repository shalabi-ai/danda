import unittest

from danda.configuration.clean_configuration import CleaningConfig
from danda.configuration.type_configuration import TypeConfig


class TestConfigSection(unittest.TestCase):

    def test_type_config_show(self):
        config = TypeConfig()

        output = config.show()

        self.assertIn("TypeConfig", output)
        self.assertIn("category_threshold", output)
        self.assertIn("numeric_threshold", output)
        self.assertIn("datetime_threshold", output)
        #self.assertIn("boolean_threshold", output)

    def test_cleaning_config_show(self):
        config = CleaningConfig()

        output = config.show()

        self.assertIn("CleaningConfig", output)
        self.assertIn("remove_duplicates", output)
        self.assertIn("strip_whitespace", output)

    def test_show_reflects_modified_values(self):
        config = TypeConfig(
            category_threshold=0.25,
            numeric_threshold=0.80,
        )

        output = config.show()

        self.assertIn("0.25", output)
        self.assertIn("0.8", output)



if __name__ == '__main__':
    unittest.main()
