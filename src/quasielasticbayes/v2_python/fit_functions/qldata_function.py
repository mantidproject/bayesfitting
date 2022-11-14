from quasielasticbayes.v2.functions.base import BaseFitFunction
from quasielasticbayes.v2.functions.qe_function import QEFunction
from quasielasticbayes.v2.functions.lorentz import Lorentzian
from numpy import ndarray
from typing import Dict, List


class QlDataFunction(QEFunction):
    def __init__(self, bg_function: BaseFitFunction, elastic_peak: bool,
                 r_x: ndarray, r_y: ndarray, start_x: float, end_x: float):
        """
        Create a quasi elastic fitting function using lorentzians
        :param bg_function: background fitting function
        :param elastic_peak: if to include an elastic peak (True/False)
        :param res_x: x values for resolution function
        :param res_y: y values for resolution function
        :param start_x: the start of the fitting range
        :param end_x: the end of the fitting range
        """
        super().__init__(bg_function, elastic_peak, r_x,
                         r_y, start_x, end_x)

    def add_single_lorentzian(self) -> None:
        """
        Add a single Lorentzian function to the qldata function
        """
        lor = Lorentzian()
        self.add_single_function(lor)

    def _add_params(self, offset: int, x0: float,
                    args: List[float]) -> List[float]:

        # adds amplitude, peak centre and FWHM
        return [args[offset], x0, args[offset + 1]]

    def _get_func_from_report(self, args: List[float]) -> List[float]:
        # skip the peak centre
        return [args[0], args[2]]

    def report(self, report_dict: Dict[str, List[float]],
               *args: float) -> Dict[str, List[float]]:
        """
        Reports the results
        :param report_dict: dict of results
        :param args: args for functions
        :returns updated results dict
        """
        report_dict = super().report(report_dict, *args)
        params = self._get_params(args)
        # manually add EISF
        if self.delta and self.conv.N_params > 2:
            BG_N_params = self.BG.N_params
            e_amp = args[BG_N_params]
            N_e = self.conv._funcs[0].N_params
            for j in range(len(self.conv._funcs)-1):
                k = j + 1
                N_qe = self.conv._funcs[k].N_params
                # params has values for delta + lorentz
                qe_amp = params[j*N_qe + N_e]
                EISF = e_amp/(e_amp + qe_amp)
                report_dict = self._add_to_report(self.conv._funcs[k]._prefix
                                                  + "EISF",
                                                  EISF, report_dict)
        return report_dict

    def _func_guess(self, full_guess: List[float]) -> List[float]:
        """
        Get the intial guess values.
        This takes into account the tied
        parameters.
        :return a list of guess parameters for the fit
        """
        # skip peak centre
        return [full_guess[0], full_guess[2]]