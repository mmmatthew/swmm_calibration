import spotpy


class ObjectiveFunction(object):
    def __init__(self, obs_config):
        self.obs_config = obs_config
        # for key, obs in obs_config.items():
        #     if not obs['calibration']['obj_fun'] in dir(spotpy.objectivefunctions):
        #         raise Exception('Objective function {} not defined in spotpy'.format(obs['calibration']['obj_fun']))

    def evaluate(self, simulation, evaluation):
        # compute similarity
        objfun = []
        for obs_name in list(evaluation.columns.values):
            # Extract data
            evalu = evaluation[obs_name]
            sim = simulation[[self.obs_config[obs_name]['swmm_node'][1]]]

            # Guarantee same time and data is compared
            data = sim.join(evalu, how='right', lsuffix='_sim', rsuffix='_eval')

            fname = self.obs_config[obs_name]['calibration']['obj_fun']
            weight = self.obs_config[obs_name]['calibration']['weight']
            objfun.append(weight * getattr(self, fname)(data))
            # objfun.append(weight * getattr(spotpy.objectivefunctions, fname)(evalu, sim))
        return sum(objfun)

    def rmse(self, data):
        return ((data.iloc[:, 0]-data.iloc[:, 1]) ** 2).mean() ** .5

    def spearman(self, data):
        return data.corr(method='spearman').iloc[0, 1]
