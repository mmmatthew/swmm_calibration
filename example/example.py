import swmm_model
import utils
import spotpy
from datetime import datetime
from datetime import timedelta
from spotpy_setup import SpotpySwmmSetup

# process data input data into the right format

# Simulation parameters
model = swmm_model.SwmmModel(
    swmm_model_template='swmm_model_template.inp',
    sim_start_dt=datetime.strptime('2016/10/06 14:06:25', '%Y/%m/%d %H:%M:%S'),  # start every 5 sec. (00:00:03 is bad)
    sim_end_dt=datetime.strptime('2016/10/06 14:20:30', '%Y/%m/%d %H:%M:%S'),
    sim_reporting_step=timedelta(seconds=5),
    forcing_data_file='19_p1_q_mid_endress_logi.txt',  # "C:/coding/swmm_calibration/example/forcing_data.txt",
    obs_config=[
        {
            "data_file": '19_s6_h_us_maxbotix.txt',
            "swmm_node": ['node', 'Exitshaft', 'Depth_above_invert']
        }
    ],
    parameter_bounds={
        's_r': [0.0, 1.0]
    }
)
model_params = [
    spotpy.parameter.Normal('s_r', 0.1, 0.05)  # Surface roughness
]

# run calibration
spotpy_setup = SpotpySwmmSetup(model, model_params)
sampler = spotpy.algorithms.sceua(spotpy_setup, dbname='SCEUA_SWMM', dbformat='csv', alt_objfun='')
sampler.sample(1)
results = sampler.getdata()

evaluation = spotpy_setup.evaluation()
evaldates = spotpy_setup.evaluation(evaldates=True)

spotpy.analyser.plot_bestmodelruns(results, evaluation, dates=evaldates, ylabel='Water head')
