import os
from os.path import join

import spotpy
from classes.swmm_model import SwmmModel
from classes.spotpy_setup import SpotpySwmmSetup


class Optimizer(object):
	"""Optimizes a model with given objective functions, parameter ranges

	"""

	def __init__(self, model: SwmmModel, cal_params, obj_fun, temp_folder):
		"""
		creates an optimizer that is ready to optimize
		:param model: initialized SwmmModel
		:param cal_params: definition of calibration parameters including ranges
		:param obj_fun: objective function to be used for calibration
		:param stopping_criteria:  stopping criteria
		:param temp_folder: where to store intermediate results
		"""

		# where to store optimization results
		self.temp_folder = temp_folder
		self.database_path = join(temp_folder, 'SCE-UA.csv')
		# set up spotpy calibrator
		self.spotpy_setup = SpotpySwmmSetup(model, cal_params, obj_fun)
		# do not save the simulation because simulation results are data frames
		# and do not support saving at this point
		self.sampler = spotpy.algorithms.sceua(
			self.spotpy_setup,
			dbname=os.path.splitext(self.database_path)[0],
			dbformat=os.path.splitext(self.database_path)[1][1:],  # result should be 'csv'
			alt_objfun='',
			save_sim=False)

	def run(self, repetitions, **kwargs):
		"""
		runs optimizer with settings
		:param repetitions: how many iterations maximum (more will be performed because some parameter combinations will
		not be accepted
		:param kwargs: keyword arguments as defined in spotpy.algorithms.sceua.sample
		"""
		self.sampler.sample(repetitions, **kwargs)

	def plot(self):
		"""plots scatter and time series of calibration run

		"""
		from helpers.plotting_utils import plot_chain, plot_density

		plot_chain(self.temp_folder, self.database_path)
		plot_density(self.temp_folder, self.database_path)
