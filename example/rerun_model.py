from os.path import join

from example import settings

from swmm_calibration.classes import experiment_runner

s = settings.Settings

temp_folder = 'results/test/1'

# plot results
runner = experiment_runner.ExperimentRunner(data_directory=temp_folder, output_file='results/experiments.csv',
                                             settings=s, experiment_metadata={'count_sensors': 1})
runner.evaluate()

# optimizer_plotting_utils.plot_chain(
#     join(temp_folder, 'iterations.csv'),
#     temp_folder
# )
