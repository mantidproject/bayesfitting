import unittest
import numpy as np
from quasielasticbayes.v2.functions.lorentz import Lorentzian
from quasielasticbayes.v2.functions.BG import LinearBG
from quasielasticbayes.v2.functions.composite import CompositeFunction


class CompositeFunctionTest(unittest.TestCase):

    def test_empty(self):
        x = np.linspace(0, 5, 6)
        c = CompositeFunction()
        y = c(x)

        for j in range(len(x)):
            self.assertAlmostEqual(y[j], 0.0, 8)

    def test_add_function(self):
        x = np.linspace(0, 5, 6)
        c = CompositeFunction()
        bg = LinearBG('f0.')

        self.assertEqual(c.N_params, 0)
        c.add_function(bg)
        self.assertEqual(c.N_params, 2)

        a = 1.3
        b = -3.1
        expect = bg(x, a, b)
        y = c(x, a, b)

        for j in range(len(x)):
            self.assertAlmostEqual(y[j], expect[j], 8)

    def test_too_few_params(self):
        x = np.linspace(0, 5, 6)
        c = CompositeFunction()
        bg = LinearBG('f0.')
        c.add_function(bg)
        with self.assertRaises(ValueError):
            _ = c(x, 1.)  # should have 2 params

    def test_too_many_params(self):
        x = np.linspace(0, 5, 6)
        c = CompositeFunction()
        bg = LinearBG('f0.')
        c.add_function(bg)

        with self.assertRaises(ValueError):
            _ = c(x, 1, 2, 3)  # should have 2 params

    def test_sum(self):
        x = np.linspace(-0.4, 0.4, 6)

        lor = Lorentzian()
        c = CompositeFunction()
        bg = LinearBG('f0.')
        c.add_function(bg)
        c.add_function(lor)

        y_l = lor(x, 20.3, 0.031, 0.3)
        y_bg = bg(x, 1, -2)

        y = c(x, 1, -2, 20.3, 0.031, 0.3)

        for j in range(5):
            self.assertAlmostEqual(y[j], y_l[j] + y_bg[j], 3)

    def test_report(self):
        report = {"old": [1]}

        lor = Lorentzian()
        c = CompositeFunction()
        c.add_function(lor)

        out = c.report(report, 3.2, -1, 2.5)
        self.assertEqual(out["f1.Amplitude"], [3.2])
        self.assertEqual(out["f1.Peak Centre"], [-1])
        self.assertEqual(out["f1.Gamma"], [2.5])
        self.assertEqual(out["old"], [1])
        self.assertEqual(len(out.keys()), 4)

    def test_report2(self):
        report = {"old": [1]}

        lor = Lorentzian()
        c = CompositeFunction()
        c.add_function(lor)
        lor2 = Lorentzian()
        c.add_function(lor2)

        out = c.report(report, 3.2, -1, 2.5, 5, 6, 7)

        self.assertEqual(out["f1.Amplitude"], [3.2])
        self.assertEqual(out["f1.Peak Centre"], [-1])
        self.assertEqual(out["f1.Gamma"], [2.5])

        self.assertEqual(out["f2.Amplitude"], [5])
        self.assertEqual(out["f2.Peak Centre"], [6])
        self.assertEqual(out["f2.Gamma"], [7])
        self.assertEqual(out["old"], [1])
        self.assertEqual(len(out.keys()), 7)

    def test_read(self):
        report = {"old": [1]}

        lor = Lorentzian()
        c = CompositeFunction()
        c.add_function(lor)

        out = c.report(report, 3.2, -1, 2.5)
        params = c.read_from_report(out, 0)
        self.assertEqual(params, [3.2, -1, 2.5])

    def test_read2(self):
        report = {"old": [1]}

        lor = Lorentzian()
        c = CompositeFunction()
        c.add_function(lor)
        lor2 = Lorentzian()
        c.add_function(lor2)

        out = c.report(report, 3.2, -1, 2.5, 5, 6, 7)
        params = c.read_from_report(out, 0)
        self.assertEqual(params, [3.2, -1, 2.5, 5, 6, 7])

    def test_guess(self):
        lor = Lorentzian()
        c = CompositeFunction()
        bg = LinearBG()
        c.add_function(bg)
        c.add_function(lor)

        self.assertEqual(c.get_guess(), [0., 0., 0.01, 0., 0.02])

    def test_bounds(self):
        lor = Lorentzian()
        c = CompositeFunction()
        bg = LinearBG()
        c.add_function(bg)
        c.add_function(lor)

        bounds = c.get_bounds()

        self.assertEqual(bounds[0], [-1., -1., 0., -1., 1.e-6])
        self.assertEqual(bounds[1], [1., 1., 1., 1., 1.])


if __name__ == '__main__':
    unittest.main()
