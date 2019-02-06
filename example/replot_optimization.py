from os.path import join

from classes import optimizer_plotting_utils
from example import settings as s

temp_folder = 'results/20190206_17.32'

# plot results
optimizer_plotting_utils.plot_density(
    join(temp_folder, 'SCE-UA.csv'),
    temp_folder,
    s.calibration_parameters
)

optimizer_plotting_utils.plot_chain(
    join(temp_folder, 'SCE-UA.csv'),
    temp_folder
)
