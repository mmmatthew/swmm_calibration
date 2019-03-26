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

    def getOptimalParams(self, how_many:int=50):
        """Returns optimal parameters and cost as dictionary

        :type how_many: int
        :return:
        """
        # Load calibration chain and find optimal for like1
        cal_data = pd.read_csv(self.database_path, sep=',')
        # sort by cost and retain best
        cal_data = cal_data.sort_values('like1', ascending=False)[:how_many]
        run_numbers = list(cal_data.index)
        # drop cost
        cal_data.drop(['like1', 'chain'], axis=1, inplace=True)
        # rename columns
        rename_dict = {}
        for k, p in self.cal_params.items():
            rename_dict['par' + k] = k
        cal_data.rename(index=str, columns=rename_dict, inplace=True)
        params = cal_data.to_dict('rows')

        return params, run_numbers
