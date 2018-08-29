import seaborn as sns
import pandas as pd





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
    sns_plot.axes[0, 0].set_ylim(0, 1.5)
    sns_plot.axes[1, 0].set_ylim(0, 0.05)
    sns_plot.axes[2, 0].set_ylim(0, 0.05)
    sns_plot.axes[3, 0].set_ylim(0, 0.05)
    sns_plot.axes[4, 0].set_ylim(0, 0.05)
    sns_plot.axes[5, 0].set_ylim(0, 1)
    sns_plot.axes[6, 0].set_ylim(0, 5)

    sns_plot.savefig("output.png")


