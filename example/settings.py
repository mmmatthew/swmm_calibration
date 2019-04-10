class Settings(object):
    swmm_executable = "C:/Program Files (x86)/EPA SWMM 5.1/swmm5.exe"
    swmm_model_template = 'swmm_model_template.inp'
    calibration_event = {
        'name': 'Exp 21',
        'start_dt': '2016/10/06 14:56:00',  # start every 5 sec. (00:00:03 is bad). Format is important
        'end_dt': '2016/10/06 15:13:00',
        'initial_conditions': {
            # initial depths
            'id_m1': 0.8,
            'id_m2': 0.4,
            'id_m3': 0.2,
            'id_4': 0.4,
            'id_9': 0.4
        }
    }
    # list of periods to be used for validation
    validation_events = [
        {
            "name": 'Exp 20',
            "start_dt": '2016/10/06 14:32:25',  # start every 5 sec. (00:00:03 is bad). Format is important
            "end_dt": '2016/10/06 14:48:00',
            'initial_conditions': {
                # initial depths
                'id_m1': 0.0,
                'id_m2': 0.4,
                'id_m3': 0.9,
                'id_4': 0.4,
                'id_9': 0.4
            }
        }
    ]
    sim_reporting_step_sec = 5  # in seconds
    forcing_data_file = 'data/all_p1_q_mid_endress_logi.txt'
    calibration_algorithm = 'sceua'
    calibration_parameters = {
        's_r': {
            "display_name": 'Surface roughness',
            'rank': 0,
            'bounds': [0, 0.03]
        },
        'r_p3': {
            "display_name": 'Roughness (pipe p3)',
            'rank': 1,
            'bounds': [0, 0.03]
        },
        'r_p7': {
            "display_name": 'Roughness (pipe p7)',
            'rank': 2,
            'bounds': [0, 0.03]
        },
        'r_px': {
            "display_name": 'Roughness (other pipes)',
            'rank': 3,
            'bounds': [0, 0.03]
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
        's6_sensor': {
            "data_file": 'data/all_s6_h_us_maxbotix.txt',
            "location": 's6',
            "data_type": 'sensor',
            "scale_factor": 0.001,
            "swmm_node": ['node', 's6', 'Depth_above_invert'],
            "calibration": {
                "obj_fun": 'rmse',
                "weight": 1  # weight should be positive if obj_fun should be minimized
            }
        }
        ,
        's5_sensor': {
            "data_file": 'data/all_s5_h_us_maxbotix_2.txt',
            "location": 's5',
            "data_type": 'sensor',
            "scale_factor": 0.001,
            "swmm_node": ['node', 's5', 'Depth_above_invert'],
            "calibration": {
                "obj_fun": 'rmse',
                "weight": 1
            }
        }
        ,
        's3_sensor': {
            "data_file": 'data/all_s3_h_us_maxbotix.txt',
            "location": 's3',
            "data_type": 'sensor',
            "scale_factor": 0.001,
            "swmm_node": ['node', 's3', 'Depth_above_invert'],
            "calibration": {
                "obj_fun": 'rmse',
                "weight": 1
            }
        },
        's6_trend': {
            "data_file": 'data/all_s6_h_us_maxbotix.txt',
            "location": 's6',
            "data_type": 'trend',
            "scale_factor": 0.001,
            "swmm_node": ['node', 's6', 'Depth_above_invert'],
            "calibration": {
                "obj_fun": 'spearman_zero',
                "weight": -1  # weight should be positive if obj_fun should be minimized
            }
        }
        ,
        's5_trend': {
            "data_file": 'data/all_s5_h_us_maxbotix_2.txt',
            "location": 's5',
            "data_type": 'trend',
            "scale_factor": 0.001,
            "swmm_node": ['node', 's5', 'Depth_above_invert'],
            "calibration": {
                "obj_fun": 'spearman_zero',
                "weight": -1
            }
        }
        ,
        's3_trend': {
            "data_file": 'data/all_s3_h_us_maxbotix.txt',
            "location": 's3',
            "data_type": 'trend',
            "scale_factor": 0.001,
            "swmm_node": ['node', 's3', 'Depth_above_invert'],
            "calibration": {
                "obj_fun": 'spearman_zero',
                "weight": -1
            }
        }
    }
    obs_config_calibration = [
        's5_trend', 's6_trend'
    ]
    obs_config_validation = [
        's3_sensor',
        's5_sensor',
        's6_sensor'
    ]