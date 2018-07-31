import swmm_model

# Simulation parameters
model = swmm_model.SwmmModel(
    swmm_model_template='testmodel.inp',
    experiment_start_date='06/24/2016',
    experiment_end_date="06/24/2016",
    experiment_start_time='13:41:24',
    experiment_end_time="13:50:00",
    forcing_data_file='forcing_data.txt',  # "C:/coding/swmm_calibration/example/forcing_data.txt",
    reporting_nodes=[
        ['node', 'Ramp', 'Total_inflow']
    ],
    parameter_bounds={
        's_r': [0.0001, 0.5]
    }
)
model_params = {
    's_r': 0.001  # surface_roughness
}

# run model
data = model.run(model_params)
print(data.head())
