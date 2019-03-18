import copy
import os
import pickle
import datetime

import pandas as pd
from . import swmm_model, objective_function

from . import optimizer


class ExperimentRunner(object):
    """Run full calibration experiment with defined settings"""

    def __init__(self, data_directory, output_file, settings, experiment_metadata):
        self.params_opt = {}
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
            obs_available=self.s.obs_available,
            obs_config_calibration=self.s.obs_config_calibration,
            obs_config_validation=self.s.obs_config_validation,
            cal_params=self.s.calibration_parameters,
            temp_folder=self.dir
        )

        # define objective function for observations
        self.obj_fun = objective_function.ObjectiveFunction(self.s.obs_available)

        # define calibrator
        self.calibrator = optimizer.Optimizer(
            model=self.model_cal,
            algorithm=self.s.calibration_algorithm,
            cal_params=self.s.calibration_parameters,
            obj_fun=self.obj_fun.evaluate,
            temp_folder=self.dir)

    def run(self, **kwargs):
        self.calibrator.run(**kwargs)
        self.calibrator.plot()
        self.params_opt, cost, run_count = self.calibrator.getOptimalParams()

        # run calibration model and print output (optional)
        # todo: print and evaluate results for all sensor locations
        sim = self.model_cal.run(named_model_params=self.params_opt,
                                 plot_results=True, plot_title='Calibration '+self.s.calibration_event['name'],
                                 obs_list=self.s.obs_config_validation, run_type='validation')
        performance = self.obj_fun.evaluate(simulation=sim,
                                            evaluation=self.model_cal.obs_validation)

        self.save_results(performance=performance, event_type='calibration', event_name=self.s.calibration_event['name'], run_count=run_count)

        self.evaluate()

    def evaluate(self):
        # evaluate calibrated model
        # run validation models and print output
        for val_event in self.s.validation_events:
            # create validation model
            model_val = swmm_model.SwmmModel(
                swmm_model_template=self.s.swmm_model_template,
                sim_start_dt=val_event['start_dt'],
                sim_end_dt=val_event['end_dt'],
                sim_reporting_step_sec=self.s.sim_reporting_step_sec,
                forcing_data_file=self.s.forcing_data_file,
                obs_available=self.s.obs_available,
                obs_config_calibration=self.s.obs_config_calibration,
                obs_config_validation=self.s.obs_config_validation,
                cal_params=self.s.calibration_parameters,
                temp_folder=self.dir
            )
            # run simulation
            sim = model_val.run(named_model_params=self.params_opt, plot_results=True,
                                plot_title='Validation with {} - calibrated on {}'.format(val_event['name'], self.s.calibration_event['name']),
                                obs_list=self.s.obs_config_validation, run_type='validation')
            # evaluate simulation
            performance = self.obj_fun.evaluate(simulation=sim,
                                                evaluation=model_val.obs_validation)
            self.save_results(performance=performance, event_type='validation', event_name=val_event['name'])

            del model_val

    def save_results(self, performance, event_type, event_name, run_count=0):
        # save params and cost to file
        df = pd.DataFrame({'par_'+key: pd.Series(value) for key, value in self.params_opt.items()})
        df['error'] = [performance]
        df['run_count'] = [run_count]
        df['type'] = [event_type]
        df['time'] = datetime.datetime.now()
        df['meta_event_val'] = event_name
        for key, value in self.experiment_metadata.items():
            df['meta_'+key] = [value]

        if not os.path.isfile(self.output_file):
            df.to_csv(self.output_file, mode='w', header=True, index=False)
        else:
            df.to_csv(self.output_file, mode='a', header=False, index=False)