import os
from os.path import join

import pandas as pd
import spotpy
from .spotpy_setup import SpotpySwmmSetup
from .swmm_model import SwmmModel

from .optimizer_plotting_utils import plot_chain, plot_density


class Optimizer(object):
    """Optimizes a model with given objective functions, parameter ranges
    """

    def __init__(self, model: SwmmModel, algorithm, cal_params, obj_fun, temp_folder):
        """
        creates an optimizer that is ready to optimize
        :param model: initialized SwmmModel
        :param algorithm: optimization algorithm used
        :param cal_params: definition of calibration parameters including ranges
        :param obj_fun: objective function to be used for calibration
        :param temp_folder: where to store intermediate results
        """

        # where to store optimization results
        self.temp_folder = temp_folder
        self.database_path = join(temp_folder, 'iterations.csv')
        # set up spotpy calibrator
        self.cal_params = cal_params
        self.spotpy_setup = SpotpySwmmSetup(model, cal_params, obj_fun)
        # do not save the simulation because simulation results are data frames
        # and do not support saving at this point
        self.sampler = getattr(spotpy.algorithms, algorithm)(
            self.spotpy_setup,
            dbname=os.path.splitext(self.database_path)[0],
            dbformat=os.path.splitext(self.database_path)[1][1:],  # result should be 'csv'
            parallel='seq',
            alt_objfun=None,  # https://github.com/thouska/spotpy/issues/161
            save_sim=False)
        # store convergence criteria
        self.convergence_criteria = None

    def run(self, repetitions, **kwargs):
        """
        runs optimizer with settings
        :param repetitions: how many iterations maximum (more will be performed because some parameter combinations will
        not be accepted
        :param kwargs: keyword arguments as defined in spotpy.algorithms.sceua.sample
        """
        self.convergence_criteria = self.sampler.sample(repetitions, **kwargs)

    def plot(self):
        """plots scatter and time series of calibration run

        """
        plot_chain(self.database_path, self.temp_folder)
        plot_density(self.database_path, self.temp_folder, self.cal_params)

    def getOptimalParams(self):
        """Returns optimal parameters and cost as dictionary

        :return:
        """
        # Load calibration chain and find optimal for like1
        cal_data = pd.read_csv(self.database_path, sep=',')
        params = cal_data.ix[cal_data['like1'].idxmax()].to_dict()
        cost = params['like1']
        # reformat parameters to match original naming
        params_reformatted = {}
        for k, p in self.cal_params.items():
            params_reformatted[k] = params['par' + k]

        return params_reformatted, cost, cal_data.shape[0]
