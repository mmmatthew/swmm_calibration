import spotpy


class ObjectiveFunction(object):
    def __init__(self, obs_config):
        self.obs_config = obs_config
        for obs in obs_config:
            if not obs['calibration']['obj_fun'] in dir(spotpy.objectivefunctions):
                raise Exception('Objective function {} not defined in spotpy'.format(obs['calibration']['obj_fun']))

    def evaluate(self, simulation, evaluation):
        # compute similarity
        objfun = []
        for obs in self.obs_config:
            evalu = list(evaluation[obs['swmm_node'][1]])
            sim = list(simulation[obs['swmm_node'][1]])
            fname = obs['calibration']['obj_fun']
            weight = obs['calibration']['weight']
            objfun.append(weight * getattr(spotpy.objectivefunctions, fname)(evalu, sim))
        return sum(objfun)
