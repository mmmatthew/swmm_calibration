# set the working directory to the location of this file
# os.chdir('C:/coding/swmm_calibration/example')

from classes import experiment_runner
from datetime import datetime
from example import settings

s = settings.Settings

for i in [5000]:
    # get temporary directory for saving working files. By default define a new one
    nowstring = datetime.strftime(datetime.now(), '%Y%m%d_%H.%M')
    temp_folder = 'results/s5/' + nowstring
    s.calibration_algorithm = 'sceua'
    exp = experiment_runner.ExperimentRunner(data_directory=temp_folder, output_file='results/experiments.csv',
                                             settings=s)
    exp.run(print_final=True, repetitions=i, kstop=5, ngs=5, pcento=0.5)
