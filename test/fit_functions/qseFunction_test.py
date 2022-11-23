import unittest
import numpy as np
from quasielasticbayes.v2.functions.BG import LinearBG
from quasielasticbayes.v2.functions.SE import StretchExp
from quasielasticbayes.v2.functions.qse_function import QSEFunction


class QSEFunctionTest(unittest.TestCase):

    def test_just_bg(self):
        x = np.linspace(0, 5, 6)
        bg = LinearBG()
        qse = QSEFunction(bg, False, x, x, 0, 6)
        y = qse(x, 1.2, 3)
        expect = 1.2*x + 3

        self.assertEqual(qse.N_params, 2)
        for j in range(len(x)):
            self.assertAlmostEqual(y[j], expect[j])

        self.assertEqual(qse.get_guess(0.1), [0., 0.])

        bounds = qse.get_bounds()
        self.assertEqual(bounds[0], [-1, -1])
        self.assertEqual(bounds[1], [1, 1])

        report = {}
        report = qse.report(report, 1, 2)
        self.assertEqual(report["N0:f1.BG gradient"], [1.])
        self.assertEqual(report["N0:f1.BG constant"], [2.])

    def test_read_just_bg(self):
        x = np.linspace(0, 5, 6)
        bg = LinearBG()
        qse = QSEFunction(bg, False, x, x, 0, 6)
        report = {}
        report = qse.report(report, 1., 2.3)
        params = qse.read_from_report(report, 0)
        self.assertEqual(params, [1., 2.3])

    def test_bg_and_delta(self):
        x = np.linspace(-5, 5, 5)
        bg = LinearBG()

        se = StretchExp()
        y = se(x, 1., 0.01, 11, .7)

        qse = QSEFunction(bg, True, x, y, -6, 6)
        y = qse(x, 1.2, 3, .2, .1)
        expect = [-3, 0.0001, 3.080, 6.000, 9.000]

        self.assertEqual(qse.get_guess(0.1), [0., 0., 1., 0.])

        bounds = qse.get_bounds()
        self.assertEqual(bounds[0], [-1, -1, 0., -1])
        self.assertEqual(bounds[1], [1, 1, np.inf, 1])

        self.assertEqual(qse.N_params, 4)
        for j in range(len(x)):
            self.assertAlmostEqual(y[j], expect[j], 3)

        report = {}
        report = qse.report(report, 1, 2, 3, 4)
        self.assertEqual(len(report.keys()), 4)
        self.assertEqual(report["N0:f1.BG gradient"], [1.])
        self.assertEqual(report["N0:f1.BG constant"], [2.])

        self.assertEqual(report["N0:f2.f1.Amplitude"], [3.])
        self.assertEqual(report["N0:f2.f1.Centre"], [4])

    def test_read_bg_and_delta(self):
        x = np.linspace(0, 5, 6)
        bg = LinearBG()
        qse = QSEFunction(bg, True, x, x, 0, 6)
        report = {}
        report = qse.report(report, 1., 2.3, .5, -.1)
        params = qse.read_from_report(report, 0)
        self.assertEqual(params, [1., 2.3, .5, -.1])

    def test_bg_and_delta_and_1_SE(self):
        x = np.linspace(-5, 5, 5)
        bg = LinearBG()

        se = StretchExp()
        y = se(x, 1., 0.01, 11, .7)

        qse = QSEFunction(bg, True, x, y, -6, 6)
        qse.add_single_SE()

        y = qse(x, .02, 1, .2, .1, 1, 10., 0.5)
        expect = [0.911, 0.972, 2.345, 1.074, 1.112]

        bounds = qse.get_bounds()
        self.assertEqual(bounds[0], [-1, -1, 0., -1, 0., 0, 0])
        self.assertEqual(bounds[1], [1, 1, np.inf, 1, 1, 100, 1])

        # shared param (peak centre)
        self.assertEqual(qse.N_params, 7)
        for j in range(len(x)):
            self.assertAlmostEqual(y[j], expect[j], 3)

        guess = qse.get_guess(0.1)
        expect = [0., 0., 1., 0., 0.1, 13.164, 0.7]
        self.assertEqual(len(guess), len(expect))
        for k in range(len(expect)):
            self.assertAlmostEqual(guess[k], expect[k], 3)

        report = {}
        report = qse.report(report, 1, 2, 3., 4, 5., 6, 7)
        self.assertEqual(len(report.keys()), 9)
        self.assertEqual(report["N1:f1.BG gradient"], [1.])
        self.assertEqual(report["N1:f1.BG constant"], [2.])

        self.assertEqual(report["N1:f2.f1.Amplitude"], [3.])
        self.assertEqual(report["N1:f2.f1.Centre"], [4])

        self.assertEqual(report["N1:f2.f2.Amplitude"], [5])
        self.assertEqual(report["N1:f2.f2.Peak Centre"], [4])
        self.assertEqual(report["N1:f2.f2.tau"], [6])
        self.assertAlmostEqual(report["N1:f2.f2.FWHM"][0], 0.110, 3)
        self.assertEqual(report["N1:f2.f2.beta"], [7])

    def test_read_bg_and_delta_and_1se(self):
        x = np.linspace(0, 5, 6)
        bg = LinearBG()
        qse = QSEFunction(bg, True, x, x, 0, 6)
        qse.add_single_SE()
        report = {}
        report = qse.report(report, 1., 2.3, .5, -.1, .1, 10, .7)
        params = qse.read_from_report(report, 1)
        self.assertEqual(params, [1., 2.3, .5, -.1, .1, 10, .7])

    def test_bg_and_1_SE(self):
        x = np.linspace(-5, 5, 5)
        bg = LinearBG()

        se = StretchExp()
        y = se(x, 1., 0.01, 11, .7)

        qse = QSEFunction(bg, False, x, y, -6, 6)
        qse.add_single_SE()

        y = qse(x, .02, 1, 1, .1, 10., 0.5)
        expect = [0.911, 0.972, 2.265, 1.074, 1.112]

        bounds = qse.get_bounds()
        self.assertEqual(bounds[0], [-1, -1, 0., -1, 0, 0])
        self.assertEqual(bounds[1], [1, 1, 1, 1, 100, 1])

        # shared param (peak centre)
        self.assertEqual(qse.N_params, 6)
        for j in range(len(x)):
            self.assertAlmostEqual(y[j], expect[j], 3)

        expect = [0., 0., 0.1, 0., 13.164, 0.7]
        guess = qse.get_guess(0.1)
        self.assertEqual(len(guess), len(expect))
        for k in range(len(expect)):
            self.assertAlmostEqual(guess[k], expect[k], 3)

        report = {}
        report = qse.report(report, 1, 2, 3., 4, 5., 6)
        self.assertEqual(len(report.keys()), 7)
        self.assertEqual(report["N1:f1.BG gradient"], [1.])
        self.assertEqual(report["N1:f1.BG constant"], [2.])

        self.assertEqual(report["N1:f2.f1.Amplitude"], [3])
        self.assertEqual(report["N1:f2.f1.Peak Centre"], [4])
        self.assertEqual(report["N1:f2.f1.tau"], [5])
        self.assertAlmostEqual(report["N1:f2.f1.FWHM"][0], 0.132, 3)
        self.assertEqual(report["N1:f2.f1.beta"], [6])

    def test_read_bg_and_1se(self):
        x = np.linspace(0, 5, 6)
        bg = LinearBG()
        qse = QSEFunction(bg, False, x, x, 0, 6)
        qse.add_single_SE()
        report = {}
        report = qse.report(report, 1., 2.3, .1, -.1, 10, .7)
        params = qse.read_from_report(report, 1)
        self.assertEqual(params, [1., 2.3, .1, -.1, 10, .7])


if __name__ == '__main__':
    unittest.main()
