import swmm_model
import utils
import spotpy
from datetime import datetime
from datetime import timedelta
from spotpy_setup import SpotpySwmmSetup

# process data input data into the right format

# Simulation parameters
model = swmm_model.SwmmModel(
    swmm_model_template='swmm_model_template_2.inp',
    sim_start_dt=datetime.strptime('2016/10/06 14:06:25', '%Y/%m/%d %H:%M:%S'),  # start every 5 sec. (00:00:03 is bad)
    sim_end_dt=datetime.strptime('2016/10/06 14:30:00', '%Y/%m/%d %H:%M:%S'),
    sim_reporting_step=timedelta(seconds=5),
    forcing_data_file='all_p1_q_mid_endress_logi.txt',  # "C:/coding/swmm_calibration/example/forcing_data.txt",
    obs_config=[
        {
            "data_file": 'all_s6_h_us_maxbotix.txt',
            "swmm_node": ['node', 'House', 'Depth_above_invert']
        }
    ],
    parameter_bounds={
        's_r': [0.0, 1.0],
        'r_p3': [0.0, 1.0],
        'r_px': [0, 1]
    }
)
model_params = [
    # spotpy.parameter.Gamma('s_r', 1.5, 0.1),  # Surface roughness
    # spotpy.parameter.Normal('r_p3', 1.5, 0.1)  # Pipe p3 roughness
    spotpy.parameter.Uniform('s_r', 0.005, 0.05),  # Surface roughness
    spotpy.parameter.Uniform('r_p3', 0.005, 0.05),  # Pipe p3 roughness
    spotpy.parameter.Uniform('r_px', 0.005, 0.05)  # Pipe p3 roughness
]

# run calibration
spotpy_setup = SpotpySwmmSetup(model, model_params)
# do not save the simulation because simulation results are data frames and do not support saving at this point
sampler = spotpy.algorithms.sceua(spotpy_setup, dbname='SCEUA_SWMM', dbformat='csv', alt_objfun='', save_sim=False)
sampler.sample(1)
results = sampler.getdata()

evaluation = spotpy_setup.evaluation()
evaldates = spotpy_setup.evaluation(evaldates=True)

spotpy.analyser.plot_bestmodelruns(results, evaluation, dates=evaldates, ylabel='Water head')
