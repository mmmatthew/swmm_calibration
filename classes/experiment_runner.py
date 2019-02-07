import os
from classes import swmm_model, objective_function, optimizer


class ExperimentRunner(object):
	"""Run full calibration experiment with defined settings"""

	def __init__(self, data_directory, output_file, settings):
		self.dir = data_directory
		self.output_file = output_file
		self.s = settings

		# create directory if it doesn't exist
		if not os.path.exists(data_directory):
			print('Making directory {}'.format(data_directory))
			os.makedirs(data_directory)

		# create model
		self.model = swmm_model.SwmmModel(
			swmm_model_template=self.s.swmm_model_template,
			sim_start_dt=self.s.sim_start_dt,
			sim_end_dt=self.s.sim_end_dt,
			sim_reporting_step=self.s.sim_reporting_step,
			forcing_data_file=self.s.forcing_data_file,
			obs_config=self.s.observations_configuration,
			cal_params=self.s.calibration_parameters,
			temp_folder=self.dir
		)

		# define objective function for observations
		self.obj_fun = objective_function.ObjectiveFunction(self.s.observations_configuration)

		# define calibrator
		self.calibrator = optimizer.Optimizer(
			model=self.model,
			cal_params=self.s.calibration_parameters,
			obj_fun=self.obj_fun.evaluate,
			temp_folder=self.dir)

	def run(self, repetitions=1000, kstop=10, ngs=8):
		self.calibrator.run(repetitions=repetitions, kstop=kstop, ngs=ngs)

elif action == 'plot':
	# plot results
	calibrator.plot()

elif action == 'get_optimal':
	params = calibrator.getOptimalParams()
	print(params)
	# run model
	data = model.run(named_model_params=params)
	print(data)
