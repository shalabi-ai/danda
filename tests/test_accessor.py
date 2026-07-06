import unittest
import pandas as pd
import danda


class AccessorTestCase(unittest.TestCase):

    def test_dataframe_has_dg_accessor(self):
        df = pd.DataFrame({"A": [1, 2]})

        assert hasattr(df, "dg")
        assert df.dg is not None

    def test_clean(self):
        p = pd.DataFrame()
        p.dg.clean()
        self.assertEqual(True, True)  # add assertion here

    def test_optimize(self):
        p = pd.DataFrame()
        p.dg.optimize()
        self.assertEqual(True, True)

    def test_report(self):
        p = pd.DataFrame()
        p.dg.report()
        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()
