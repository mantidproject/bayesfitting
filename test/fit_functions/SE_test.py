import unittest
import numpy as np
from quasielasticbayes.v2.functions.SE import StretchExp


class StretchExpTest(unittest.TestCase):

    def test_call_1(self):
        x = np.linspace(-0.4, 0.4, 6)

        se = StretchExp()

        y = se(x, 0.0, 1, 25.0, 0.5)
        # from Mantid version 6.5
        expect = [0.192, 0.299, 1.001, 1.001, 0.299, 0.192]

        self.assertEqual(len(y), len(expect))
        for j in range(len(y)):
            self.assertAlmostEqual(y[j], expect[j], 3)

    def test_call_2(self):
        x = np.linspace(-0.4, 0.4, 6)

        se = StretchExp()

        y = se(x, 0.1, 0.5, 25.0, 0.5)
        # from Mantid version 6.5
        expect = [0.083, 0.109, 0.201, 2.2993, 0.264, 0.122]

        self.assertEqual(len(y), len(expect))
        for j in range(len(y)):
            self.assertAlmostEqual(y[j], expect[j], 3)

    def test_report(self):
        report = {"old": [1]}

        se = StretchExp()
        out = se.report(report, 0.1, 1, 10, .5)

        self.assertEqual(out["Amplitude"], [1])
        self.assertEqual(out["Peak Centre"], [0.1])
        self.assertEqual(out["tau"], [10.])
        self.assertEqual(out["beta"], [0.5])
        self.assertEqual(out["old"], [1])
        self.assertEqual(len(out.keys()), 5)

    def test_N_params(self):
        se = StretchExp()
        self.assertEqual(se.N_params, 4)

    def test_guess(self):
        se = StretchExp()
        self.assertEqual(se.get_guess(), [0, 0.01, 0.01, 0.01])

    def test_bounds(self):
        se = StretchExp()
        bounds = se.get_bounds()
        self.assertEqual(bounds[0], [-1., 0, 0, 0])
        self.assertEqual(bounds[1], [1., 1, 100., 1.])


if __name__ == '__main__':
    unittest.main()
