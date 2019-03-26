import random
import math


class ObjectiveFunction(object):
    def __init__(self, obs_config):
        self.obs_config = obs_config
        # for key, obs in obs_config.items():
        #     if not obs['calibration']['obj_fun'] in dir(spotpy.objectivefunctions):
        #         raise Exception('Objective function {} not defined in spotpy'.format(obs['calibration']['obj_fun']))

    def evaluate(self, simulation, evaluation):
        # decide whether to print of values:
        print_fitness = False
        if random.choices([True, False], weights=[1, 100])[0]:
            print_fitness = True
        # compute similarity
        objfun = []
        for obs_name in list(evaluation.columns.values):
            # Extract data
            evalu = evaluation[obs_name]
            # Simulations extracted as dataframe so that join is possible
            sim = simulation[[obs_name]]

            # Guarantee same time and data is compared
            data = sim.join(evalu, how='inner', lsuffix='_sim', rsuffix='_eval')

            fname = self.obs_config[obs_name]['calibration']['obj_fun']
            weight = self.obs_config[obs_name]['calibration']['weight']
            objfun.append(weight * getattr(self, fname)(data))

        return sum(objfun)

    def rmse(self, data):
        return ((data.iloc[:, 0] - data.iloc[:, 1]) ** 2).mean() ** .5

    def spearman(self, data):
        # a modified spearman correlation coefficient to account for zeros
        # timesteps with zeros on both sides are good
        both_zeros = (data.iloc[:, 0] == 0) & (data.iloc[:, 1] == 0)
        fraction_matching_zeros = sum(both_zeros) / len(both_zeros)

        # timesteps without any zeros can be checked with pearson
        no_zeros = (data.iloc[:, 0] != 0) & (data.iloc[:, 1] != 0)
        fraction_no_zeros = sum(no_zeros) / len(no_zeros)
        # if there is very little data, then don't compute spearman
        if sum(no_zeros) < 10:
            spearman = 0
        else:
            spearman = data[no_zeros].corr(method='spearman').iloc[0, 1]
            # catch the failing spearman
            if math.isnan(spearman):
                spearman = 0

        # combine both to make hybrid spearman
        spearman_hybrid = fraction_matching_zeros + spearman * fraction_no_zeros


        return spearman_hybrid

    def spearman_zero(self, data):
        # make maximum zero instead of one
        return self.spearman(data) - 1
