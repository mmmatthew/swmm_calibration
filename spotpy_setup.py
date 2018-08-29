import spotpy


class SpotpySwmmSetup(object):
    def __init__(self, model, prior_dist):
        self.model = model
        self.prior_dist = prior_dist

    def parameters(self):
        return spotpy.parameter.generate(self.prior_dist)

    def simulation(self, vector):
        simulations = self.model.run(*vector)
        return simulations

    def evaluation(self, evaldates=False):
        if evaldates:
            return self.model.eval_dates
        else:
            return self.model.observations

    def objectivefunction(self, simulation, evaluation, params=None):

        # compute similarity
        objfun = []
        for obs in self.model.obs_config:
            evalu = list(evaluation[obs['swmm_node'][1]])
            sim = list(simulation[obs['swmm_node'][1]])
            objfun.append(spotpy.objectivefunctions.rsquared(evalu, sim))
        return -sum(objfun)


