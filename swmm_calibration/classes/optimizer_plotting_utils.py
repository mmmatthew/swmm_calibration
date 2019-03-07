import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from os.path import join

# self is an optimizer as defined in optimizer.py


def plot_chain(database_path, temp_folder):
    sns.set(style="ticks")

    data = pd.read_csv(database_path, sep=',')

    data['iteration'] = data.index

    # reshape data
    data_reshaped = data.melt(id_vars=['iteration', 'chain'], value_name='param_value', var_name='param_name')

    # Define a palette to ensure that colors will be
    # shared across the facets
    palette = dict(zip(data_reshaped.chain.unique(),
                       sns.color_palette("rocket_r", len(data_reshaped.chain.unique()))))

    # Plot the lines on two facets
    sns_plot = sns.relplot(x="iteration", y="param_value",
                hue="chain", row="param_name", palette=palette,
                aspect=5, facet_kws=dict(sharex=False, sharey=False),
                kind="line", legend="full", data=data_reshaped)

    sns_plot.savefig(join(temp_folder, "calibration_chain.png"))
    plt.clf()


# plot parameter distributions
def plot_density(database_path, temp_folder, cal_params, uselast: int=200):
    sns.set(style="dark")

    # read data
    data = pd.read_csv(database_path, sep=',')
    data['iteration'] = data.index
    # remove burn-in
    data = data.iloc[-uselast:]


    variables = ['par'+k for k, p in cal_params.items()]
    names = [p['display_name'] for k, p in cal_params.items()]

    g = sns.PairGrid(data, vars=variables, diag_sharey=False)
    g.map_lower(sns.kdeplot)
    g.map_upper(sns.scatterplot, size=1)
    g.map_diag(sns.kdeplot)
    g.savefig(join(temp_folder, "parameter_sampling_distributions.png"))
    plt.clf()
