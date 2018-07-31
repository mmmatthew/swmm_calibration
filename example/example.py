import swmm_model

model = swmm_model.SwmmModel()
params = {
    'forcing_data_file': "C:/coding/swmm_calibration/example/forcing_data.txt"
}
model.run(params)
