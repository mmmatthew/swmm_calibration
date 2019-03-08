from os.path import join

from example import settings

from swmm_calibration.classes import optimizer_plotting_utils

s = settings.Settings

temp_folder = 'results/test/1'

# plot results
optimizer_plotting_utils.plot_density(
    join(temp_folder, 'iterations.csv'),
    temp_folder,
    s.calibration_parameters
)

# optimizer_plotting_utils.plot_chain(
#     join(temp_folder, 'iterations.csv'),
#     temp_folder
# )
