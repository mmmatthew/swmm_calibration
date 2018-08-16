import os
import subprocess
from string import Template
import pandas as pd
import numpy as np
from os.path import join
from datetime import datetime
from datetime import timedelta
from swmmtoolbox import swmmtoolbox


class SwmmModel(object):
    """
    Input:  data_start: e.g. datetime(2016,10,6,14,10)
            data_end: e.g. datetime(2016,10,6,14,20)
            model_template
            parameter_bounds: physical parameter boundaries
    Output: Initialized model instance with forcing data (inflow to experiment site) and evaluation data (water level in basement of house)
    """
    temp_folder = 'C:/_temp/swmm'
    swmm_executable = "C:/Program Files (x86)/EPA SWMM 5.1/swmm5.exe"
    # define input and output
    temp_model = join(temp_folder, 'model.inp')
    output_file = join(temp_folder, 'output.out')
    report_file = join(temp_folder, 'report.rpt')

    def __init__(self, swmm_model_template, sim_start_dt, sim_end_dt, sim_reporting_step, forcing_data_file, evaluation_data_file, reporting_nodes, parameter_bounds):

        with open(swmm_model_template, 'r') as t:
            self.swmm_model_template = Template(t.read())
        self.sim_start_dt = sim_start_dt
        self.sim_end_dt = sim_end_dt
        self.sim_reporting_step = sim_reporting_step
        self.forcing_data_file = forcing_data_file
        self.evaluation_data_file = evaluation_data_file
        self.reporting_nodes = reporting_nodes
        self.parameter_bounds = parameter_bounds
        # Read observation data and filter to fit experiment duration
        self.observations = pd.read_csv(
            filepath_or_buffer=evaluation_data_file,
            index_col=0,
            parse_dates=[0],
            infer_datetime_format=True,
            dayfirst=False,
            sep=';')
        shift = timedelta(seconds=1)
        self.observations = self.observations.loc[sim_start_dt+shift : sim_end_dt-shift]

        self.eval_data = list(self.observations['value'])
        self.eval_dates = list(self.observations.index)

    def run(self, *model_params):
        """
        Runs the SWMM model with specific parameters. The following parameters can be passed.
        :param multiple unnamed params: 1st: surface roughness
        :return: the simulation of the model
        """
        model_params = {
            's_r': model_params[0]
        }
        return self._run(model_params)

    def _run(self, model_params):

        # Check model params
        if not self.check_parameters(model_params):
            return self.eval_data * -10000

        # Apply model params to model
        self.apply_parameters(model_params)

        # Run model
        with open(os.devnull, "w") as f:
            subprocess.call([self.swmm_executable, self.temp_model, self.report_file, self.output_file],
                            stdout=f)

        # read simulation output
        data = swmmtoolbox.extract(self.output_file, ' '.join([','.join(x) for x in self.reporting_nodes]))
        res_col_name = '_'.join(self.reporting_nodes[0])

        # only give results for time steps where evaluation data exists
        # synced = pd.merge(
        #     left=data, left_on=res_col_name,
        #     right=self.observations, right_on='value',
        #     how='inner')
        synced = data.join(self.observations, how='inner')

        # self.eval_data = list(synced['value'])
        # self.eval_dates = list(synced.index)

        return list(synced[res_col_name])

    def apply_parameters(self, model_params):
        # apply simulation params to model
        params = {
            'forcing_data_file': self.forcing_data_file,
            'sim_start_time': datetime.strftime(self.sim_start_dt, '%H:%M:%S'),
            'sim_end_time': datetime.strftime(self.sim_end_dt, '%H:%M:%S'),
            'sim_start_date': datetime.strftime(self.sim_start_dt, '%m/%d/%Y'),
            'sim_end_date': datetime.strftime(self.sim_end_dt, '%m/%d/%Y'),
            'sim_report_step': str(self.sim_reporting_step),
            's_r': model_params['s_r']
        }

        # apply parameters to input
        input_mod = self.swmm_model_template.substitute(params)
        with open(self.temp_model, 'w') as f:
            f.write(input_mod)

    def check_parameters(self, model_params):
        # check that parameters are within acceptable bounds
        for param_name, value in model_params.items():
            if value < self.parameter_bounds[param_name][0] or value > self.parameter_bounds[param_name][1]:
                print('''
                The following combination was ignored:
                surface roughness: {s_r} = {s_r_val}
                ##############################
                '''.format(
                    s_r=param_name,
                    s_r_val=value
                ))
                return False
        return True

    def sync_timeseries(self, simulation, evaluation):
        """
        Formats simulation data so each value corresponds to a data point in evaluation,
        where certain time steps are missing
        """
