from classes.optimizer_plotting_utils import plot_chain, plot_density

temp_folder = 'c:/_temp/swmm/dev'
plot_chain(temp_folder, 'iterations.csv')
plot_density(temp_folder, 'iterations.csv')
