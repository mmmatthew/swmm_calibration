from pyswmm import Simulation
import subprocess
from string import Template
import pandas
from os.path import join
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

    def __init__(self, swmm_model_template, experiment_start_time, experiment_end_time, experiment_start_date,
                 experiment_end_date, forcing_data_file, reporting_nodes, parameter_bounds):
        self.swmm_model_template = swmm_model_template
        self.experiment_start_date = experiment_start_date
        self.experiment_end_date = experiment_end_date
        self.experiment_start_time = experiment_start_time
        self.experiment_end_time = experiment_end_time
        self.forcing_data_file = forcing_data_file
        self.reporting_nodes = reporting_nodes
        self.parameter_bounds = parameter_bounds

    def run(self, model_params):
        return self._run(model_params)

    def _run(self, model_params):

        # check that parameters are acceptable
        for param_name, value in model_params:
            if value < self.parameter_bounds[param_name][0] or value > self.parameter_bounds[param_name][1]:
                print
                '''
                The following combination was ignored:
                surface roughness: %s_r
                ##############################
                '''.format({'s_r':model_params['s_r']})
                return 1

        # simulation params
        params = {
            'forcing_data_file': self.forcing_data_file,
            'experiment_start_date': self.experiment_start_date,
            'experiment_end_date': self.experiment_end_date,
            'experiment_start_time': self.experiment_start_time,
            'experiment_end_time': self.experiment_end_time,
            's_r': model_params['s_r']
        }
        # define input and output
        temp_model = join(self.temp_folder, 'temp.inp')
        # apply parameters to input
        with open(self.swmm_model_template, 'r') as t:
            template = Template(t.read())
            input_mod = template.substitute(params)
        with open(temp_model, 'w') as f:
            f.write(input_mod)
        output_file = join(self.temp_folder, 'testoutput.out')
        report_file = join(self.temp_folder, 'testreport.rpt')
        subprocess.call([self.swmm_executable, temp_model, report_file, output_file])

        # read simulation output
        data = swmmtoolbox.extract(output_file, ' '.join([','.join(x) for x in self.reporting_nodes]))

        return data
