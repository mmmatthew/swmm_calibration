from os.path import join

from example import settings as s

from swmm_calibration.classes import optimizer_plotting_utils

temp_folder = 'results/20190206_17.32'

# plot results
optimizer_plotting_utils.plot_density(
    join(temp_folder, 'iterations.csv'),
    temp_folder,
    s.calibration_parameters
)

optimizer_plotting_utils.plot_chain(
    join(temp_folder, 'iterations.csv'),
    temp_folder
)
