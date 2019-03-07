import pandas as pd
from datetime import datetime
import csv

def format_resample(
        input_file,                 # full path to data file to be read
        output_file,                # path to file where data should be saved
        aggregation_frequency=None, # resampling frequency of data
        aggregation_type='mean'     # aggregation method for data
):
    # reads CSV data in pandas format and outputs data in SWMM format
    # resamples the data to 1-second frequency

    # read data
    data = pd.read_csv(input_file,
                       parse_dates=[0],
                       index_col=0,
                       infer_datetime_format=True,
                       dayfirst=True,
                       # date_parser=date_parser,
                       sep=';')

    # aggregate per second, interpolate
    data = data.resample('S')
    data = data.mean()
    data = data.resample('S')
    data = data.interpolate(method='linear')

    data['datetime'] = data.index
    data['date'] = data['datetime'].apply(lambda x: x.strftime('%m/%d/%Y'))
    data['time'] = data['datetime'].apply(lambda x: x.strftime('%H:%M:%S'))

    data.to_csv(output_file,
                sep=' ',
                columns=['date', 'time', 'value'],
                # quoting=3,  #csv.QUOTE_NONE,
                index=False,
                header=False)


def resample(
        input_file,  # full path to data file to be read
        output_file,  # path to file where data should be saved
        aggregation_period='S',  # resampling frequency of data
        aggregation_type='mean'  # aggregation method for data
):
    # converts pandas formatted file to SWMM formatted file
    # read data
    data = pd.read_csv(input_file,
                       parse_dates=[0],
                       index_col=0,
                       infer_datetime_format=True,
                       dayfirst=True,
                       # date_parser=date_parser,
                       sep=';')

    # aggregate per second, interpolate
    data = data.resample(aggregation_period)
    data = data.mean()
    data = data.resample(aggregation_period)
    data = data.interpolate(method='linear')

    data['datetime'] = data.index

    data.to_csv(output_file,
                sep=';',
                columns=['datetime', 'value'],
                # quoting=3,  #csv.QUOTE_NONE,
                index=False,
                header=True)


def format(
        input_file,  # full path to data file to be read
        output_file,  # path to file where data should be saved
        aggregation_frequency=None,  # resampling frequency of data
        aggregation_type='mean'  # aggregation method for data
):
    # converts pandas formatted file to SWMM formatted file
    # read data
    data = pd.read_csv(input_file,
                       parse_dates=[0],
                       index_col=0,
                       infer_datetime_format=True,
                       dayfirst=True,
                       # date_parser=date_parser,
                       sep=';')

    data['datetime'] = data.index
    data['date'] = data['datetime'].apply(lambda x: x.strftime('%m/%d/%Y'))
    data['time'] = data['datetime'].apply(lambda x: x.strftime('%H:%M:%S'))

    data.to_csv(output_file,
                sep=' ',
                columns=['date', 'time', 'value'],
                # quoting=3,  #csv.QUOTE_NONE,
                index=False,
                header=False)
