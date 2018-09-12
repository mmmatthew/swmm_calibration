from datetime import datetime, timedelta
from string import Template

swmm_model_template_file = 'swmm_model_template_2.inp'
temp_model = 'C:/_temp/swmm/model_realization.inp'
temp_forcing_data_file = 'C:/_temp/swmm/forcing_data.txt'
sim_start_dt = datetime.strptime('2016/10/06 14:06:25', '%Y/%m/%d %H:%M:%S')  # start every 5 sec. (00:00:03 is bad)
sim_end_dt = datetime.strptime('2016/10/06 14:21:00', '%Y/%m/%d %H:%M:%S')
sim_reporting_step = timedelta(seconds=5)

model_params = {
    's_r': 0.011,
    'r_p3': 0.04,
    'r_p7': 0.01,
    'r_px': 0.009,
    'c_m1': 0.9,
    'c_w1': 9.3,
}

# apply simulation params to model
params = {
    'forcing_data_file': temp_forcing_data_file,
    'sim_start_time': datetime.strftime(sim_start_dt, '%H:%M:%S'),
    'sim_end_time': datetime.strftime(sim_end_dt, '%H:%M:%S'),
    'sim_start_date': datetime.strftime(sim_start_dt, '%m/%d/%Y'),
    'sim_end_date': datetime.strftime(sim_end_dt, '%m/%d/%Y'),
    'sim_report_step': str(sim_reporting_step)
}
params.update(model_params)

with open(swmm_model_template_file, 'r') as t:
    swmm_model_template = Template(t.read())

# apply parameters to input
input_mod = swmm_model_template.substitute(params)
with open(temp_model, 'w') as f:
    f.write(input_mod)

