import unittest
import pandas as pd
import pandas.testing as pdt
from danda.plugins.report_collector import ReportCollector
from danda.plugins.clean.emptay_spaces import EmptySpacesPlugin


class TestEmptySpacesPlugin(unittest.TestCase):
    def setUp(self):
        self.report = ReportCollector()
        self.plugin = EmptySpacesPlugin(self.report)

    def test_execute_strips_whitespace(self):
        df = pd.DataFrame(
            {
                "name": [" Alice ", "Bob  ", "  Charlie"],
                "city": [" London", "Paris ", " Berlin "],
            }
        )

        expected = pd.DataFrame(
            {
                "name": ["Alice", "Bob", "Charlie"],
                "city": ["London", "Paris", "Berlin"],
            }
        )

        result = self.plugin._execute(df, self.report)

        pdt.assert_frame_equal(result, expected)

    def test_execute_leaves_non_string_columns_unchanged(self):
        df = pd.DataFrame(
            {
                "name": [" Alice "],
                "age": [30],
                "salary": [1000.5],
            }
        )

        result = self.plugin._execute(df, self.report)

        pdt.assert_series_equal(result["age"], df["age"])
        pdt.assert_series_equal(result["salary"], df["salary"])

    def test_execute_does_not_modify_original_dataframe(self):
        df = pd.DataFrame({"name": [" Alice "]})
        original = df.copy(deep=True)

        self.plugin._execute(df, self.report)

        pdt.assert_frame_equal(df, original)

    def test_get_report_data_returns_changed_columns(self):
        before = pd.DataFrame(
            {
                "name": [" Alice "],
                "city": ["Paris"],
                "age": [25],
            }
        )

        after = self.plugin._execute(before, self.report)

        changed = self.plugin._get_report_data(
            before,
            after,
            self.report,
        )

        self.assertEqual(changed, ["name"])

    def test_get_report_data_returns_empty_when_no_changes(self):
        before = pd.DataFrame(
            {
                "name": ["Alice"],
                "city": ["Paris"],
            }
        )

        after = self.plugin._execute(before, self.report)

        changed = self.plugin._get_report_data(
            before,
            after,
            self.report,
        )

        self.assertEqual(changed, [])

    def test_report_with_changes(self):
        message = self.plugin._report(["name", "city"], self.report)

        self.assertEqual(
            message,
            "Stripped leading/trailing whitespace from columns: name, city",
        )

    def test_report_without_changes(self):
        message = self.plugin._report([], self.report)

        self.assertEqual(
            message,
            "No leading or trailing whitespace found.",
        )


if __name__ == "__main__":
    unittest.main()


if __name__ == '__main__':
    unittest.main()
