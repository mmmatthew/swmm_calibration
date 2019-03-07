# set the working directory to the location of this file
# os.chdir('C:/coding/swmm_calibration/example')

import copy
from datetime import datetime

from example import settings

from swmm_calibration.classes import experiment_runner

scenarios = [

    {
        'name': 's5',
        'selection': ['s5']
    },
    {
        'name': 's6',
        'selection': ['s6']
    },
    {
        'name': 's3',
        'selection': ['s3']
    },
    {
        'name': 'all',
        'selection': ['s3', 's5', 's6']
    }
]

for scenario in scenarios:
    s = copy.deepcopy(settings.Settings)
    # get temporary directory for saving working files. By default define a new one
    nowstring = datetime.strftime(datetime.now(), '%Y%m%d_%H.%M')
    temp_folder = 'results/availability/' + scenario['name']
    s.calibration_algorithm = 'sceua'
    s.observations_configuration = list(s.obs_available[i] for i in scenario['selection'])
    exp = experiment_runner.ExperimentRunner(data_directory=temp_folder, output_file='results/experiments.csv',
                                             settings=s)
    exp.run(print_final=True, repetitions=5000, kstop=5, ngs=5, pcento=0.5)
