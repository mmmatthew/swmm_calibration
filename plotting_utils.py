import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# plot optimization chain results
def plot_chain(database_file):
    sns.set(style="ticks")

    data = pd.read_csv(database_file, sep=',')

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

    # adapt axis range
    # sns_plot.axes[0, 0].set_ylim(0, 1.5)
    # sns_plot.axes[1, 0].set_ylim(0, 0.05)
    # sns_plot.axes[2, 0].set_ylim(0, 0.05)
    # sns_plot.axes[3, 0].set_ylim(0, 0.05)
    # sns_plot.axes[4, 0].set_ylim(0, 0.05)
    # sns_plot.axes[5, 0].set_ylim(0, 1)
    # sns_plot.axes[6, 0].set_ylim(0, 5)

    sns_plot.savefig("calibration_chain.png")


# plot parameter distributions
def plot_density(database_file, burn_in=0.75):
    sns.set(style="dark")

    # read data
    data = pd.read_csv(database_file, sep=',')
    data['iteration'] = data.index
    # remove burn-in
    data = data.iloc[int(data.shape[0]*burn_in):]
    # reshape data
    # data = data.melt(id_vars=['iteration', 'chain'], value_name='param_value', var_name='param_name')

    # Set up the matplotlib figure
    f, axes = plt.subplots(3, 2, figsize=(9, 6), sharex=False)


    # parameters
    params = [
        {
            "code": 'pars_r',
            "name": 'Surface roughness'
        },
        {
            "code": 'parr_p3',
            "name": 'Roughness (pipe p3)'
        },
        {
            "code": 'parr_p7',
            "name": 'Roughness (pipe p7)'
        },
        {
            "code": 'parr_px',
            "name": 'Roughness (other pipes)'
        },
        {
            "code": 'parc_m1',
            "name": 'Capacity manhole m1'
        },
        {
            "code": 'parc_w1',
            "name": 'Capacity weir w1'
        }
    ]
    for ax, p in zip(axes.flat, params):
        sns.distplot(data[p['code']], hist=False, rug=True, color="r", ax=ax, axlabel=p['name'])

    f.tight_layout()
    f.show()

    f.savefig("parameter kernel")
