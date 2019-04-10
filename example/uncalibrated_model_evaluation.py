from datetime import datetime
from example import settings

from swmm_calibration.classes import experiment_runner

s = settings.Settings

for i in [5000]:
    # get temporary directory for saving working files. By default define a new one
    nowstring = datetime.strftime(datetime.now(), '%Y%m%d_%H.%M')
    temp_folder = 'results/test/uncalibrated/' + nowstring
    s.obs_config_validation = [
        's3_sensor',
        's5_sensor',
        's6_sensor'
    ]
    s.obs_config_calibration = [
        's3_sensor',
        's5_sensor',
        's6_sensor'
    ]
    exp = experiment_runner.ExperimentRunner(data_directory=temp_folder, output_file='results/uncalibrated_experiments.csv',
                                             settings=s, experiment_metadata={'count_sensors': 1}, evaluation_count=10)
    performance = exp.evaluate_uncalibrated(count=10)

    print(performance)
