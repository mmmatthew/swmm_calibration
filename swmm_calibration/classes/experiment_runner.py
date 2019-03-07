import copy
import os
import pickle

import pandas as pd
from classes import swmm_model, objective_function

from swmm_calibration.classes import optimizer


class ExperimentRunner(object):
    """Run full calibration experiment with defined settings"""

    def __init__(self, data_directory, output_file, settings, experiment_metadata):
        self.dir = data_directory
        self.output_file = output_file
        self.s = copy.deepcopy(settings)
        self.experiment_metadata = copy.deepcopy(experiment_metadata)

        # create directory if it doesn't exist
        if not os.path.exists(data_directory):
            print('Making directory {}'.format(data_directory))
            os.makedirs(data_directory)

        # write settings to file in temp dir
        with open(os.path.join(self.dir, 'settings.pickle'), 'wb') as file:
            pickle.dump(settings, file)

        # create calibration model
        self.model_cal = swmm_model.SwmmModel(
            swmm_model_template=self.s.swmm_model_template,
            sim_start_dt=self.s.calibration_event['start_dt'],
            sim_end_dt=self.s.calibration_event['end_dt'],
            sim_reporting_step_sec=self.s.sim_reporting_step_sec,
            forcing_data_file=self.s.forcing_data_file,
            obs_config=self.s.observations_configuration,
            cal_params=self.s.calibration_parameters,
            temp_folder=self.dir
        )


        # define objective function for observations
        self.obj_fun = objective_function.ObjectiveFunction(self.s.observations_configuration)

        # define calibrator
        self.calibrator = optimizer.Optimizer(
            model=self.model_cal,
            algorithm=self.s.calibration_algorithm,
            cal_params=self.s.calibration_parameters,
            obj_fun=self.obj_fun.evaluate,
            temp_folder=self.dir)

    def run(self, print_final=False, **kwargs):
        self.calibrator.run(**kwargs)
        self.calibrator.plot()
        params, cost = self.calibrator.getOptimalParams()

        # save params and cost to file
        df = pd.DataFrame({key: pd.Series(value) for key, value in params.items()})
        df['cost_calibration'] = [cost]
        if not os.path.isfile(self.output_file):
            df.to_csv(self.output_file, mode='w', header=True)
        else:
            df.to_csv(self.output_file, mode='a', header=False)

        # run calibration model and print output (optional)
        # todo: print and evaluate results for all sensor locations
        if print_final:
            sim = self.model_cal.run(named_model_params=params, plot_results=True, plot_title='Validation '+self.s.calibration_event['name'])

        # run validation models and print output
        for val_event in self.s.validation_events:
            # create validation model
            model_val = swmm_model.SwmmModel(
                swmm_model_template=self.s.swmm_model_template,
                sim_start_dt=val_event['start_dt'],
                sim_end_dt=val_event['end_dt'],
                sim_reporting_step_sec=self.s.sim_reporting_step_sec,
                forcing_data_file=self.s.forcing_data_file,
                obs_config=self.s.observations_configuration,
                cal_params=self.s.calibration_parameters,
                temp_folder=self.dir
            )
            # run simulation
            sim = model_val.run(named_model_params=params, plot_results=True, plot_title='Validation '+val_event['name'])
            # evaluate simulation
