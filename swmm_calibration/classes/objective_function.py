import spotpy


class ObjectiveFunction(object):
    def __init__(self, obs_config):
        self.obs_config = obs_config
        for key, obs in obs_config.items():
            if not obs['calibration']['obj_fun'] in dir(spotpy.objectivefunctions):
                raise Exception('Objective function {} not defined in spotpy'.format(obs['calibration']['obj_fun']))

    def evaluate(self, simulation, evaluation):
        # compute similarity
        objfun = []
        for obs_name in list(evaluation.columns.values):
            evalu = list(evaluation[self.obs_config[obs_name]['swmm_node'][1]])
            sim = list(simulation[self.obs_config[obs_name]['swmm_node'][1]])
            fname = self.obs_config[obs_name]['calibration']['obj_fun']
            weight = self.obs_config[obs_name]['calibration']['weight']
            objfun.append(weight * getattr(spotpy.objectivefunctions, fname)(evalu, sim))
        return sum(objfun)
