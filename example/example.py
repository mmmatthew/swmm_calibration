import swmm_model
import utils
import spotpy
from datetime import datetime
from datetime import timedelta
from spotpy_setup import SpotpySwmmSetup

# process data input data into the right format

# Simulation parameters
model = swmm_model.SwmmModel(
    swmm_model_template='swmm_model_template_3.inp',
    sim_start_dt=datetime.strptime('2016/10/07 12:44:30', '%Y/%m/%d %H:%M:%S'),  # start every 5 sec. (00:00:03 is bad)
    sim_end_dt=datetime.strptime('2016/10/07 13:03:20', '%Y/%m/%d %H:%M:%S'),
    sim_reporting_step=timedelta(seconds=5),
    forcing_data_file='data/all_p1_q_mid_endress_logi.txt',  # "C:/coding/swmm_calibration/example/forcing_data.txt",
    obs_config=[
        {
            "data_file": 'data/all_s6_h_us_maxbotix.txt',
            "swmm_node": ['node', 's6', 'Depth_above_invert']
        }, {
            "data_file": 'data/all_s5_h_us_maxbotix_2.txt',
            "swmm_node": ['node', 's5', 'Depth_above_invert'],
        }, {
            "data_file": 'data/all_s3_h_us_maxbotix.txt',
            "swmm_node": ['node', 's3', 'Depth_above_invert'],
        }
    ],
    parameter_bounds={
        's_r': [0.0, 1.0],
        'r_p3': [0.0, 1.0],
        'r_p7': [0.0, 1.0],
        'r_px': [0, 1],
        'c_m1': [0, 1],
        'c_w1': [0, 10]
    }
)
model_params = [
    # spotpy.parameter.Gamma('s_r', 1.5, 0.1),  # Surface roughness
    # spotpy.parameter.Normal('r_p3', 1.5, 0.1)  # Pipe p3 roughness
    spotpy.parameter.Uniform('s_r', 0.005, 0.05),  # Surface roughness
    spotpy.parameter.Uniform('r_p3', 0.005, 0.05),  # Pipe p3 roughness
    spotpy.parameter.Uniform('r_p7', 0.005, 0.05),  # Pipe p7 roughness
    spotpy.parameter.Uniform('r_px', 0.005, 0.05),  # all other Pipe roughness
    spotpy.parameter.Uniform('c_m1', 0, 1),  # sewer inlet discharge coefficient into manhole m1
    spotpy.parameter.Uniform('c_w1', 0, 10)  # weir discharge coefficient
]

# run calibration
spotpy_setup = SpotpySwmmSetup(model, model_params)
# do not save the simulation because simulation results are data frames and do not support saving at this point
sampler = spotpy.algorithms.sceua(spotpy_setup, dbname='SCE-UA', dbformat='csv', alt_objfun='', save_sim=False)
sampler.sample(1500, ngs=6, pcento=0.01)
results = sampler.getdata()
