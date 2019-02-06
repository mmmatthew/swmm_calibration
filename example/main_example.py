import os
# set the working directory to the location of this file
# os.chdir('C:/coding/swmm_calibration/example')

from classes import swmm_model, objective_function, optimizer
from datetime import datetime
import example.settings as s


nowstring = datetime.strftime(datetime.now(), '%Y%m%d_%H.%M')
temp_folder = 'results/' + nowstring
if not os.path.exists(temp_folder):
    print('Making directory {}'.format(temp_folder))
    os.makedirs(temp_folder)

# create model
model = swmm_model.SwmmModel(
    swmm_model_template=s.swmm_model_template,
    sim_start_dt=s.sim_start_dt,
    sim_end_dt=s.sim_end_dt,
    sim_reporting_step=s.sim_reporting_step,
    forcing_data_file=s.forcing_data_file,
    obs_config=s.observations_configuration,
    cal_params=s.calibration_parameters,
    temp_folder=temp_folder
)

# define objective function for observations
obj_fun = objective_function.ObjectiveFunction(s.observations_configuration)

# define calibrator
calibrator = optimizer.Optimizer(
    model=model,
    cal_params=s.calibration_parameters,
    obj_fun=obj_fun.evaluate,
    temp_folder=temp_folder)

# run calibration
calibrator.run(repetitions=1000, kstop=10, ngs=8)

# plot results
calibrator.plot()
