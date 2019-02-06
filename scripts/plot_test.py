from classes.optimizer_plotting_utils import plot_chain, plot_density

temp_folder = 'c:/_temp/swmm/dev'
plot_chain(temp_folder, 'SCE-UA.csv')
plot_density(temp_folder, 'SCE-UA.csv')
