from quasielasticbayes.v2.base import BaseFitFunction
from numpy import ndarray
import numpy as np
from typing import Dict, List


class CompositeFunction(BaseFitFunction):
    def __init__(self, prefix: str = ''):
        super().__init__(0, prefix)
        self._funcs = []

    def add_function(self, func: BaseFitFunction):
        # the params for the last added function are first
        func.add_to_prefix(f'f{len(self._funcs)+1}')
        self._funcs.append(func)
        self._N_params += func.N_params

    def split_args(self, args: List[float]) -> List[List[float]]:
        """
        Split the single args list into a list of lists
        for use with functions
        """
        j = 0
        split = []
        for func in self._funcs:
            N = func.N_params
            split.append(list(args[j:j+N]))
            j += N
        return split

    def __call__(self, x: ndarray, *args: float) -> ndarray:
        """
        Implement a sum of functions.
        Need to follow the expected
        form for scipy
        """
        if len(self._funcs) == 0:
            return np.zeros(len(x))
        elif len(args) != self.N_params:
            raise ValueError(f"Expected {self.N_params} args, got {len(args)}")

        fun_args = self.split_args(args)
        result = np.zeros(len(x))
        for j, func in enumerate(self._funcs):
            result += func(x, *fun_args[j])
        return result

    def report(self, report_dict: Dict[str, List[float]],
               *args: float) -> Dict[str, List[float]]:
        """
        returns the fit parameters as a dict
        """
        if len(args) != self.N_params:
            raise ValueError(f"Expected {self.N_params} args, got {len(args)}")

        fun_args = self.split_args(args)
        for j, func in enumerate(self._funcs):
            report_dict = func.report(report_dict, *fun_args[j])
        return report_dict
