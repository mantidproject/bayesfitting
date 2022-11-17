from quasielasticbayes.v2.functions.qse_function import QSEFunction
from quasielasticbayes.v2.fitting.scipy_fit import scipy_curve_fit
from quasielasticbayes.v2.utils.spline import spline
from quasielasticbayes.v2.utils.general import get_background_function
from quasielasticbayes.v2.log_likelihood import loglikelihood

from numpy import ndarray
import numpy as np
from typing import Dict, List


def qse_data_main(sample: Dict[str, ndarray], res: Dict[str, ndarray],
                  BG_type: str, start_x: float, end_x: float,
                  elastic: bool,
                  results: Dict[str, ndarray],
                  params: List[float] = None) -> (Dict[str, ndarray],
                                                  List[float]):
    """
    The main function for calculating QSEdata.
    This uses the stretch exponential
    Steps are:
    1. Interpolate and crop the data to have same bins
    2. Fit BG + delta (if elastic=True)
    3. Fit BG + delta (if elastic=True) + stretch exp
    4. Calculate loglikelihood for fit
    5. Report results
    :param sample: dict containing the sample x, y and e data (keys = x, y, e)
    :param res: dict containg the resolution x, y data (keys = x, y)
    :param BG_type: the type of BG ("none", "flat", "linear")
    :param start_x: the start x for the calculation
    :param end_x: the end x for the calculation
    :param elastic: if to include the elastic peak
    :param results: dict of results
    :param params: initial values, if None (default) a guess will be made
    :result dict of the fit parameters, the new x array
    """
    # step 0
    BG = get_background_function(BG_type)
    N = 1
    # step 1
    x_data = sample['x']
    dx = x_data[1] - x_data[0]
    new_x = np.linspace(start_x, end_x, int((end_x - start_x)/dx))

    sy = spline(sample['x'], sample['y'], new_x)
    se = spline(sample['x'], sample['e'], new_x)
    ry = spline(res['x'], res['y'], new_x)

    scale_factor = np.max(sy)*(np.max(new_x)-np.min(new_x))

    func = QSEFunction(BG, elastic, new_x, ry, start_x, end_x)
    func.add_single_SE()

    # get estimate for FWHM -> tau
    y_max = np.max(sy)
    tmp = np.where(sy > y_max/2.)
    est_FWHM = new_x[tmp[0][-1]] - new_x[tmp[0][0]]

    guess = None
    if params is not None:
        guess = params
    else:
        guess = func.get_guess(est_FWHM)
    lower, upper = func.get_bounds()
    (chi2, hess_det, params, fit) = scipy_curve_fit(new_x, sy, se,
                                                    func, guess,
                                                    lower, upper)

    params = list(params)
    results = func.report(results, *params)

    prob_name = f'N{N}:loglikelihood'
    if prob_name in results:
        results[prob_name].append(loglikelihood(len(sy), chi2,
                                                hess_det,
                                                func.N_peaks,
                                                scale_factor))
    else:
        results[prob_name] = [loglikelihood(len(sy), chi2,
                                            hess_det,
                                            func.N_peaks,
                                            scale_factor)]

    return results, new_x
