import unittest
from quasielasticbayes.v2.functions.qse_function import QSEFunction
from quasielasticbayes.v2.functions.BG import LinearBG
from quasielasticbayes.v2.QSE import qse_data_main
import numpy as np
import os.path

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


"""
Paramater result are from Mantid v6.5 on Windows
"""


class QSEV2Test(unittest.TestCase):
    def test_one(self):
        sx, sy, se = np.load(os.path.join(DATA_DIR, 'sample_data_red.npy'))
        rx, ry, re = np.load(os.path.join(DATA_DIR, 'qse_res.npy'),
                             allow_pickle=True)

        sample = {'x': sx, 'y': sy, 'e': se}
        resolution = {'x': rx, 'y': ry}
        results = {}

        results, new_x = qse_data_main(sample, resolution,
                                       "linear", -0.4, 0.4, True, results)

        # not from Mantid
        self.assertAlmostEqual(results['N1:loglikelihood'][0], -389.94, 2)

        # from Mantid, if not then as a comment
        self.assertAlmostEqual(results['N1:f2.f2.FWHM'][0], 0.055, 3)
        self.assertAlmostEqual(results['N1:f2.f2.beta'][0], 0.794, 3)  # 0.752

        # dont compare amp to Mantid due to different scaling etc.
        self.assertAlmostEqual(results['N1:f2.f2.Amplitude'][0], 0.167, 2)

    def test_two(self):
        """
        Want to check that two calls to the function will append the results
        correctly. So if we use the same input data as above, we expect
        both values to be the same for every item in the dict.
        """
        sx, sy, se = np.load(os.path.join(DATA_DIR, 'sample_data_red.npy'))
        rx, ry, re = np.load(os.path.join(DATA_DIR, 'qse_res.npy'),
                             allow_pickle=True)

        sample = {'x': sx, 'y': sy, 'e': se}
        resolution = {'x': rx, 'y': ry}
        results = {}

        results, new_x = qse_data_main(sample, resolution,
                                       "linear", -0.4, 0.4,
                                       True, results)

        # use the previous results to make it faster
        lbg = LinearBG()
        qse = QSEFunction(lbg, True, rx, ry, -.4, 0.4)
        qse.add_single_SE()
        params = qse.read_from_report(results, 1, 0)

        # call it again
        results, new_x = qse_data_main(sample, resolution,
                                       "linear", -0.4, 0.4,
                                       True, results, params)

        for key in results.keys():
            self.assertEqual(len(results[key]), 2)
            tmp = results[key]
            self.assertAlmostEqual(tmp[0], tmp[1], 3)


if __name__ == '__main__':
    unittest.main()
