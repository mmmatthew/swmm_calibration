from classes import swmm_model, objective_function, optimizer
from datetime import datetime
from datetime import timedelta

# process data input data into the right format

nowstring = datetime.strftime(datetime.now(), '%Y%m%d_%H.%M')
temp_folder = 'results/' + nowstring
calibration_parameters = {
    's_r': {
        'rank': 0,
        'bounds': [0.005, 0.05]
    },
    'r_p3': {
        'rank': 1,
        'bounds': [0.005, 0.05]
    },
    'r_p7': {
        'rank': 2,
        'bounds': [0.005, 0.05]
    },
    'r_px': {
        'rank': 3,
        'bounds': [0.005, 0.05]
    },
    'c_m1': {
        'rank': 4,
        'bounds': [0, 1]
    },
    'c_w1': {
        'rank': 5,
        'bounds': [0, 10]
    }
}
observations_configuration = [
    {
        "data_file": 'data/all_s6_h_us_maxbotix.txt',
        "swmm_node": ['node', 's6', 'Depth_above_invert'],
        "calibration": {
            "obj_fun": 'rsquared',
            "weight": 1
        }
    }, {
        "data_file": 'data/all_s5_h_us_maxbotix_2.txt',
        "swmm_node": ['node', 's5', 'Depth_above_invert'],
        "calibration": {
            "obj_fun": 'rsquared',
            "weight": 1
        }
    }, {
        "data_file": 'data/all_s3_h_us_maxbotix.txt',
        "swmm_node": ['node', 's3', 'Depth_above_invert'],
        "calibration": {
            "obj_fun": 'rsquared',
            "weight": 1
        }
    }
]

# create model
model = swmm_model.SwmmModel(
    swmm_model_template='swmm_model_template.inp',
    sim_start_dt=datetime.strptime('2016/10/06 14:06:25', '%Y/%m/%d %H:%M:%S'),  # start every 5 sec. (00:00:03 is bad)
    sim_end_dt=datetime.strptime('2016/10/06 14:21:00', '%Y/%m/%d %H:%M:%S'),
    sim_reporting_step=timedelta(seconds=5),
    forcing_data_file='data/all_p1_q_mid_endress_logi.txt',  # "C:/coding/swmm_calibration/example/forcing_data.txt",
    obs_config=observations_configuration,
    cal_params=calibration_parameters,
    temp_folder=temp_folder
)

# define objective function for observations
obj_fun = objective_function.ObjectiveFunction(observations_configuration)

# define calibrator
calibrator = optimizer.Optimizer(
    model=model,
    cal_params=calibration_parameters,
    obj_fun=obj_fun.evaluate,
    temp_folder=temp_folder)

# run calibration
calibrator.run(repetitions=100, kstop=10, ngs=8)

# plot results
calibrator.plot()
