import os
import subprocess
from string import Template
import pandas as pd
import numpy as np
from os.path import join
from datetime import datetime
from datetime import timedelta
from swmmtoolbox import swmmtoolbox


def read_floodx_file(evaluation_data_file):
    return pd.read_csv(
        filepath_or_buffer=evaluation_data_file,
        index_col=0,
        parse_dates=[0],
        infer_datetime_format=True,
        dayfirst=True,
        sep=';')

def resample_interpolate(data, period):
    # aggregate per second, interpolate
    data = data.resample(period)
    data = data.mean()
    data = data.resample(period)
    return data.interpolate(method='linear')


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
    temp_forcing_data_file = join(temp_folder, 'forcing_data.txt')
    observations = None
    eval_data = None
    eval_dates = None

    def __init__(self, swmm_model_template, sim_start_dt, sim_end_dt, sim_reporting_step, forcing_data_file, obs_config,
                 parameter_bounds):

        with open(swmm_model_template, 'r') as t:
            self.swmm_model_template = Template(t.read())
        self.sim_start_dt = sim_start_dt
        self.sim_end_dt = sim_end_dt
        self.sim_reporting_step = sim_reporting_step
        self.parameter_bounds = parameter_bounds
        self.obs_config = obs_config

        # Read observation data and filter to fit experiment duration
        self.read_observations(obs_config)

        # Read forcing data and reformat
        self.read_forcing(forcing_data_file)


    def read_forcing(self, forcing_data_file):
        data = read_floodx_file(forcing_data_file)
        data = resample_interpolate(data, 'S')
        data['datetime'] = data.index
        data['date'] = data['datetime'].apply(lambda x: x.strftime('%m/%d/%Y'))
        data['time'] = data['datetime'].apply(lambda x: x.strftime('%H:%M:%S'))

        data.to_csv(self.temp_forcing_data_file,
                    sep=' ',
                    columns=['date', 'time', 'value'],
                    # quoting=3,  #csv.QUOTE_NONE,
                    index=False,
                    header=False)

    def read_observations(self, obs_config):
        for obs in obs_config:
            # read data
            obs_data = read_floodx_file(obs['data_file'])
            # resample: aggregate per second, interpolate
            period = '{0}S'.format(int(self.sim_reporting_step.total_seconds()))
            obs_data = resample_interpolate(obs_data, period)
            # clip to simulation time
            shift = timedelta(seconds=int(self.sim_reporting_step.total_seconds()))
            obs_data = obs_data.loc[self.sim_start_dt + shift: self.sim_end_dt - shift]

            self.eval_data = list(obs_data['value'])
            self.eval_dates = list(obs_data.index)
            # set column name and append to obs
            if self.observations is None:
                self.observations = obs_data.rename(index=str, columns={'value': obs['swmm_node'][1]})
            else:
                self.observations[obs['swmm_node'][1]] = obs_data

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
        data = swmmtoolbox.extract(self.output_file, ' '.join([','.join(x['swmm_node']) for x in self.obs_config]))

        return data

    def apply_parameters(self, model_params):
        # apply simulation params to model
        params = {
            'forcing_data_file': self.temp_forcing_data_file,
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
