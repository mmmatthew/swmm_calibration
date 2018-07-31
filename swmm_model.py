from pyswmm import Simulation
import subprocess
from string import Template
import pandas
from os.path import join


class SwmmModel(object):
    """
    Input:  data_start: e.g. datetime(2016,10,6,14,10)
            data_end: e.g. datetime(2016,10,6,14,20)
            model_template
            parameter_bounds: physical parameter boundaries
    Output: Initialized model instance with forcing data (inflow to experiment site) and evaluation data (water level in basement of house)
    """
    temp_folder = './'  #'C:/_temp'
    swmm_executable = "C:/Program Files (x86)/EPA SWMM 5.1/swmm5.exe"
    model_file = 'testmodel.inp'

    def __init__(self, data_start=None, data_end=None, model_template=None, parameter_bounds=None, calibration_points=[]):
        self.d_f = data_start
        self.d_e = data_end
        self.m_t = model_template
        self.p_b = parameter_bounds
        self.c_p = calibration_points

    def run(self, params):
        return self._run(params)

    @classmethod
    def _run(cls, params):
        # define input and output
        temp_model = join(cls.temp_folder, 'temp.inp')
        # apply parameters to input
        with open(cls.model_file, 'r') as t:
            template = Template(t.read())
            input_mod = template.substitute(params)
        with open(temp_model, 'w') as f:
            f.write(input_mod)
        output_file = join(cls.temp_folder, 'testoutput.out')
        subprocess.call([cls.swmm_executable, temp_model, output_file])
