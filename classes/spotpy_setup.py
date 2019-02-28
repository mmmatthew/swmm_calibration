import spotpy


class SpotpySwmmSetup(object):
    def __init__(self, model, calib_params, objective_function):
        self.model = model
        self.objectivefunction = objective_function
        self.prior_dist = [None]*len(calib_params)
        # remap calibration parameters into list format
        for key, value in calib_params.items():
            self.prior_dist[value['rank']] = spotpy.parameter.Uniform(key, value['bounds'][0], value['bounds'][1])

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




