import unittest
import pandas as pd

from danda.plugins.clean.drop_duplicates import DropDuplicatesPlugin
from danda.plugins.report_collector import ReportCollector
import danda  # noqa: F401  # registers the pandas accessor
from pandas._testing import assert_frame_equal


class TestDropDuplicates(unittest.TestCase):

    def setUp(self):
        self.report = ReportCollector()
        self.plugin = DropDuplicatesPlugin(self.report)

    def test_drop_duplicate_rows(self):
        df = pd.DataFrame({
            "A": [1, 2, 2, 3],
            "B": ["a", "b", "b", "c"],
        })

        result = self.plugin.run(df)

        expected = pd.DataFrame({
            "A": [1, 2, 3],
            "B": ["a", "b", "c"],
        }, index=[0, 1, 3])

        assert_frame_equal(result, expected)

    def test_report_data(self):
        df = pd.DataFrame({
            "A": [1, 2, 2, 3],
            "B": ["a", "b", "b", "c"],
        })

        self.plugin.run(df)

        expected = {
            "clean": {
                "DropDuplicates": 1
            }
        }

        self.assertEqual(self.report.data, expected)

    def test_report(self):
        df = pd.DataFrame({
            "A": [1, 2, 2, 3],
            "B": ["a", "b", "b", "c"],
        })

        self.plugin.run(df)

        expected = {
            "clean": {
                "DropDuplicates": "Number of deleted rows: 1"
            }
        }

        self.assertEqual(self.report.report, expected)

    def test_no_duplicates(self):
        df = pd.DataFrame({
            "A": [1, 2, 3],
            "B": ["a", "b", "c"],
        })

        result = self.plugin.run(df)

        pd.testing.assert_frame_equal(result, df.reset_index(drop=True))

        self.assertEqual(
            self.report.data,
            {
                "clean": {
                    "DropDuplicates": 0
                }
            },
        )

    def test_ignore_index_true(self):
        df = pd.DataFrame(
            {
                "A": [1, 1, 2],
                "B": ["x", "x", "y"],
            },
            index=[10, 20, 30],
        )

        df.dg.config.cleaning.remove_duplicates_ignore_index = True

        plugin = DropDuplicatesPlugin(ReportCollector())
        result = plugin.run(df)

        expected = pd.DataFrame(
            {
                "A": [1, 2],
                "B": ["x", "y"],
            }
        )

        assert_frame_equal(result, expected)
        self.assertEqual(list(result.index), [0, 1])


if __name__ == "__main__":
    unittest.main()


if __name__ == '__main__':
    unittest.main()
