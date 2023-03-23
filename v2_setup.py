import numpy
from distutils.core import Extension
from os.path import join
from typing import Sequence
from Cython.Build import cythonize


def create_extension(fq_name: str,
                     sources: Sequence[str]) -> Extension:
    """
    Create an extension module
    :param fq_name: The final fully-qualified name of the module
    :param sources: List of relative paths from this file to the sources
    :return: An Extension class to be built
    """
    return Extension(name=fq_name,
                     sources=sources,
                     include_dirs=[numpy.get_include()])


def source_paths(dirname: str, filenames: Sequence[str]) -> Sequence[str]:
    """
    :param dirname: A relative path to the list of source files
    :return: A list of relative paths to the given sources in the directory
    """
    return [join(dirname, filename) for filename in filenames]


def get_v2_extensions(PACKAGE_NAME):
    module_source_map = {
        f'{PACKAGE_NAME}.v2.functions.base':
            [join('fit_functions', 'base.py')],
        f'{PACKAGE_NAME}.v2.functions.BG':
            [join('fit_functions', 'BG.py')],
        f'{PACKAGE_NAME}.v2.functions.delta':
            [join('fit_functions', 'delta_function.py')],
        f'{PACKAGE_NAME}.v2.functions.lorentz':
            [join('fit_functions', 'lorentz.py')],
        f'{PACKAGE_NAME}.v2.functions.gaussian':
            [join('fit_functions', 'gaussian.py')],
        f'{PACKAGE_NAME}.v2.functions.composite':
            [join('fit_functions', 'composite_fun.py')],
        f'{PACKAGE_NAME}.v2.functions.convolution':
            [join('fit_functions', 'conv_with_res.py')],
        f'{PACKAGE_NAME}.v2.functions.qldata_function':
            [join('fit_functions', 'qldata_function.py')],
        f'{PACKAGE_NAME}.v2.functions.qe_function':
            [join('fit_functions', 'quasielastic_function.py')],
        f'{PACKAGE_NAME}.v2.functions.SE_fix':
            [join('fit_functions', 'stretch_exp_fixed.py')],
        f'{PACKAGE_NAME}.v2.functions.SE':
            [join('fit_functions', 'stretch_exp.py')],
        f'{PACKAGE_NAME}.v2.functions.qse_function':
            [join('fit_functions', 'qse.py')],
        f'{PACKAGE_NAME}.v2.functions.exp_decay':
            [join('fit_functions', 'exp_decay.py')],
        f'{PACKAGE_NAME}.v2.functions.qse_fixed':
            [join('fit_functions', 'qse_fixed.py')],


        f'{PACKAGE_NAME}.v2.fitting.fit_utils':
            [join('fit_engines', 'fit_utils.py')],
        f'{PACKAGE_NAME}.v2.fitting.fit_engine':
            [join('fit_engines', 'fit_engine.py')],
        f'{PACKAGE_NAME}.v2.fitting.scipy_engine':
            [join('fit_engines', 'scipy_fit_engine.py')],
        f'{PACKAGE_NAME}.v2.fitting.gofit_engine':
            [join('fit_engines', 'gofit_engine.py')],

        f'{PACKAGE_NAME}.test_helpers.template_fit_test':
            [join('test_helpers', 'template_test_fit.py')],
        f'{PACKAGE_NAME}.test_helpers.fitting_data':
            [join('test_helpers', 'fitting_data.py')],
        f'{PACKAGE_NAME}.test_helpers.template_scipy_fit':
            [join('test_helpers', 'template_scipy_fit_test.py')],

        f'{PACKAGE_NAME}.v2.log_likelihood':
            ['log_likelihood.py'],

        f'{PACKAGE_NAME}.v2.workflow.template':
            [join('workflows', 'workflow_template.py')],

        f'{PACKAGE_NAME}.v2.workflow.model_template':
            [join('workflows', 'model_selection',
                  'model_template.py')],
        f'{PACKAGE_NAME}.v2.workflow.QlData':
            [join('workflows', 'model_selection',
                  'qldata_main.py')],
        f'{PACKAGE_NAME}.v2.workflow.QSE':
            [join('workflows', 'model_selection',
                  'qse_main.py')],
        f'{PACKAGE_NAME}.v2.workflow.MuonExpDecay':
            [join('workflows', 'model_selection',
                  'muon_exp_decay_main.py')],

        f'{PACKAGE_NAME}.v2.workflow.grid_template':
            [join('workflows', 'grid_search',
                  'grid_search_template.py')],
        f'{PACKAGE_NAME}.v2.workflow.qse_search':
            [join('workflows', 'grid_search',
                  'qse_grid_search.py')],




        f'{PACKAGE_NAME}.v2.utils.general':
            [join('utils', 'general.py')],
        f'{PACKAGE_NAME}.v2.utils.spline':
            [join('utils', 'spline.py')],
        f'{PACKAGE_NAME}.v2.utils.crop_data':
            [join('utils', 'crop_data.py')]

            }
    path = join('src', PACKAGE_NAME)
    return cythonize([create_extension(name,
                     source_paths(str(join(path, 'v2_python')), sources)) for
                     name, sources in module_source_map.items()])
