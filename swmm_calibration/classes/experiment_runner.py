import copy
import os
import pickle
import datetime

import pandas as pd
from . import swmm_model, objective_function

from . import optimizer


class ExperimentRunner(object):
    """Run full calibration experiment with defined settings"""
    params_opt = []
    params_opt_run_numbers = []
    calibration_errors = []

    def __init__(self, data_directory, output_file, settings, experiment_metadata, experiment_name=None, evaluation_count=50):
        self.dir = data_directory
        self.experiment_name = experiment_name
        self.output_file = output_file
        self.s = copy.deepcopy(settings)
        self.experiment_metadata = copy.deepcopy(experiment_metadata)
        self.evaluation_count = evaluation_count  # how many of the model runs should be evaluated?

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
            initial_conditions=self.s.calibration_event['initial_conditions'],
            sim_start_dt=self.s.calibration_event['start_dt'],
            sim_end_dt=self.s.calibration_event['end_dt'],
            sim_event_name='{}_cal{}'.format(experiment_name, self.s.calibration_event['name']),
            sim_reporting_step_sec=self.s.sim_reporting_step_sec,
            forcing_data_file=self.s.forcing_data_file,
            obs_available=self.s.obs_available,
            obs_config_calibration=self.s.obs_config_calibration,
            obs_config_validation=self.s.obs_config_validation,
            cal_params=self.s.calibration_parameters,
            temp_folder=self.dir,
            swmm_exexcutable=self.s.swmm_executable
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
        # return the 50 best model parameter sets, inlcuding run number for each
        self.params_opt, self.params_opt_run_numbers, self.calibration_errors = self.calibrator.getOptimalParams(how_many=self.evaluation_count)

        # run calibration model for all parameter sets and print output for first (supposedly best one)
        for idx, (paramset, run_number, cal_err) in enumerate(zip(self.params_opt, self.params_opt_run_numbers, self.calibration_errors)):
            sim = self.model_cal.run(named_model_params=paramset,
                                     plot_results=(idx == 0),
                                     plot_title='{} - Cal {}'.format(self.experiment_name, self.s.calibration_event['name']),
                                     obs_list=self.s.obs_config_validation, run_type='validation')

            # The performance here is different from the cost in the iterations file
            # because we are using validation observations: usually just sensor data
            performance = self.obj_fun.evaluate(simulation=sim,
                                                evaluation=self.model_cal.obs_validation)

            self.save_results(performance=performance, params=paramset, event_type='calibration', event_name=self.s.calibration_event['name'], run_count=run_number, cal_err=cal_err)

        self.evaluate()

    def evaluate_uncalibrated(self, count=50):
        # evaluate model performance with parameter ranges provided
        # define sampler
        self.calibrator = optimizer.Optimizer(
            model=self.model_cal,
            algorithm='lhs',  # USE LATIN HYPERCUBE SAMPLING
            cal_params=self.s.calibration_parameters,
            obj_fun=self.obj_fun.evaluate,
            temp_folder=self.dir)

        # sample (and run)
        self.calibrator.run(repetitions=count)
        # plot sampling
        self.calibrator.plot()

        # return the 50 best model parameter sets, including run number for each
        self.params_opt, self.params_opt_run_numbers, self.calibration_errors = self.calibrator.getOptimalParams(how_many=count)
        # run calibration model for all parameter sets and print output for first (supposedly best one)
        for idx, (paramset, run_number, cal_err) in enumerate(zip(self.params_opt, self.params_opt_run_numbers, self.calibration_errors)):
            sim = self.model_cal.run(named_model_params=paramset,
                                     plot_results=(idx == 0), plot_title='Uncalibrated '+self.s.calibration_event['name'],
                                     obs_list=self.s.obs_config_validation, run_type='validation')

            # The performance here is different from the cost in the iterations file
            # because we are using validation observations: usually just sensor data
            performance = self.obj_fun.evaluate(simulation=sim,
                                                evaluation=self.model_cal.obs_validation)

            self.save_results(performance=performance, params=paramset, event_type='uncalibrated', event_name=self.s.calibration_event['name'], run_count=run_number, cal_err=cal_err)

    def evaluate(self):
        # evaluate calibrated model
        # run validation models and print output and save to file
        for val_event in self.s.validation_events:
            # create validation model
            model_val = swmm_model.SwmmModel(
                swmm_model_template=self.s.swmm_model_template,
                initial_conditions=val_event['initial_conditions'],
                sim_start_dt=val_event['start_dt'],
                sim_end_dt=val_event['end_dt'],
                sim_event_name='{}_cal{}_val{}'.format(self.experiment_name, self.s.calibration_event['name'], val_event['name']),
                sim_reporting_step_sec=self.s.sim_reporting_step_sec,
                forcing_data_file=self.s.forcing_data_file,
                obs_available=self.s.obs_available,
                obs_config_calibration=self.s.obs_config_calibration,
                obs_config_validation=self.s.obs_config_validation,
                cal_params=self.s.calibration_parameters,
                temp_folder=self.dir
            )
            # run simulation for each optimal parameter
            for idx, (paramset, run_number, cal_err) in enumerate(zip(self.params_opt, self.params_opt_run_numbers, self.calibration_errors)):
                sim = model_val.run(named_model_params=paramset, plot_results=(idx == 0),  # only plot first (best)
                                    plot_title='{} - Val {} - Cal {}'.format(self.experiment_name, val_event['name'], self.s.calibration_event['name']),
                                    obs_list=self.s.obs_config_validation, run_type='validation')
                # evaluate simulation
                performance = self.obj_fun.evaluate(simulation=sim,
                                                    evaluation=model_val.obs_validation)
                self.save_results(performance=performance, params=paramset, event_type='validation', event_name=val_event['name'], run_count=run_number, cal_err=cal_err)

            del model_val

    def save_results(self, performance, params, event_type, event_name, run_count=None, cal_err=None):
        # save params and cost to file
        df = pd.DataFrame({'par_'+key: pd.Series(value) for key, value in params.items()})
        df['error'] = [performance]
        df['run_count'] = [run_count]
        df['cal_err'] = [cal_err]
        df['type'] = [event_type]
        df['time'] = datetime.datetime.now()
        df['meta_event_val'] = event_name
        for key, value in self.experiment_metadata.items():
            df['meta_'+key] = [value]

        if not os.path.isfile(self.output_file):
            df.to_csv(self.output_file, mode='w', header=True, index=False)
        else:
            df.to_csv(self.output_file, mode='a', header=False, index=False)
