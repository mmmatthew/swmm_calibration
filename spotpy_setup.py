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

    def objectivefunction(self, simulation, evaluation):

        # compute similarity
        eval = list(evaluation[self.model.obs_config[0]['swmm_node'][1]])
        sim = list(simulation['_'.join(self.model.obs_config[0]['swmm_node'])])
        objectivefunction = -spotpy.objectivefunctions.rmse(eval, sim)
        return objectivefunction


