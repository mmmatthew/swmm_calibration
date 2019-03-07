class Settings(object):
    swmm_model_template = 'swmm_model_template.inp'
    calibration_event = {
        'name': 'Exp 20',
        'start_dt': '2016/10/06 14:06:25',  # start every 5 sec. (00:00:03 is bad). Format is important
        'end_dt': '2016/10/06 14:21:00'
    }
    # list of periods to be used for validation
    validation_events = [
        {
            "name": 'Exp 20',
            "start_dt": '2016/10/06 14:06:25',  # start every 5 sec. (00:00:03 is bad). Format is important
            "end_dt": '2016/10/06 14:21:00'
        }
    ]
    sim_reporting_step_sec = 5  # in seconds
    forcing_data_file = 'data/all_p1_q_mid_endress_logi.txt'
    calibration_algorithm = 'sceua'
    calibration_parameters = {
        's_r': {
            "display_name": 'Surface roughness',
            'rank': 0,
            'bounds': [0.005, 0.1]
        },
        'r_p3': {
            "display_name": 'Roughness (pipe p3)',
            'rank': 1,
            'bounds': [0.005, 0.05]
        },
        'r_p7': {
            "display_name": 'Roughness (pipe p7)',
            'rank': 2,
            'bounds': [0.005, 0.05]
        },
        'r_px': {
            "display_name": 'Roughness (other pipes)',
            'rank': 3,
            'bounds': [0.005, 0.05]
        },
        'c_m1': {
            "display_name": 'Capacity manhole m1',
            'rank': 4,
            'bounds': [0, 1]
        },
        'c_m3': {
            "display_name": 'Capacity manhole m3',
            'rank': 5,
            'bounds': [0, 1]
        },
        'c_w1': {
            "display_name": 'Capacity weir w1',
            'rank': 6,
            'bounds': [0, 10]
        }
    }
    obs_available = {
        's6': {
            "data_file": 'data/all_s6_h_us_maxbotix.txt',
            "scale_factor": 0.001,
            "swmm_node": ['node', 's6', 'Depth_above_invert'],
            "calibration": {
                "obj_fun": 'rmse',
                "weight": 1  # weight should be positive if obj_fun should be maximized
            }
        }
        ,
        's5': {
            "data_file": 'data/all_s5_h_us_maxbotix_2.txt',
            "scale_factor": 0.001,
            "swmm_node": ['node', 's5', 'Depth_above_invert'],
            "calibration": {
                "obj_fun": 'rmse',
                "weight": 1
            }
        }
        ,
        's3': {
            "data_file": 'data/all_s3_h_us_maxbotix.txt',
            "scale_factor": 0.001,
            "swmm_node": ['node', 's3', 'Depth_above_invert'],
            "calibration": {
                "obj_fun": 'rmse',
                "weight": 1
            }
        }
    }
    observations_configuration = [
        obs_available['s3'],
        obs_available['s5'],
        obs_available['s6'],
    ]
