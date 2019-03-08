# set the working directory to the location of this file
# os.chdir('C:/coding/swmm_calibration/example')

from datetime import datetime
from example import settings

from swmm_calibration import experiment_runner

s = settings.Settings

for i in [5000]:
    # get temporary directory for saving working files. By default define a new one
    nowstring = datetime.strftime(datetime.now(), '%Y%m%d_%H.%M')
    temp_folder = 'results/test/1' # + nowstring
    exp = experiment_runner.ExperimentRunner(data_directory=temp_folder, output_file='results/experiments.csv',
                                             settings=s, experiment_metadata={'count_sensors': 1})
    exp.run(repetitions=1000, kstop=5, ngs=5, pcento=0.5)
