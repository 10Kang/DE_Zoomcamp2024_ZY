import io
import pandas as pd
import requests
import os
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/'
    
    # only last quater of 2020, 10,11,12
    # List of file names
    file_names = [
        'green_tripdata_2020-10.csv.gz',
        'green_tripdata_2020-11.csv.gz',
        'green_tripdata_2020-12.csv.gz'
    ]

    # list for storing df
    dfs = []

    # map data types 
    taxi_dtypes = {
                    'VendorID': pd.Int64Dtype(),
                    'passenger_count': pd.Int64Dtype(),
                    'trip_distance': float,
                    'RatecodeID':pd.Int64Dtype(),
                    'store_and_fwd_flag':str,
                    'PULocationID':pd.Int64Dtype(),
                    'DOLocationID':pd.Int64Dtype(),
                    'payment_type': pd.Int64Dtype(),
                    'fare_amount': float,
                    'extra':float,
                    'mta_tax':float,
                    'tip_amount':float,
                    'tolls_amount':float,
                    'improvement_surcharge':float,
                    'total_amount':float,
                    'congestion_surcharge':float
                }

    # parse the date column
    parse_dates = ['lpep_pickup_datetime','lpep_dropoff_datetime']

    # iterate through the file
    for file_name in file_names:
        # join filepath 
        filepath = os.path.join(url,file_name)

        # load file
        df = pd.read_csv(filepath, compression='gzip',sep=',',dtype=taxi_dtypes,parse_dates=parse_dates)
        
        # append 
        dfs.append(df)
        print(filepath)

    return pd.concat(dfs, ignore_index=True)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
