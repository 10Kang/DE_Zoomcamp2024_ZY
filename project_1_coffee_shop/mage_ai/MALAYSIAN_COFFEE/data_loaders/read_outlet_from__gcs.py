import pandas as pd
from google.cloud import storage
import os
import io
from google.oauth2 import service_account

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

credentials_location = '/home/src/gcp_terraform.json'
credentials = service_account.Credentials.from_service_account_file(credentials_location)

@data_loader
def gcp_csv_to_df():
    bucket_name = 'malaysian_coffee_chain'
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob('raw/outlet/outlet.csv')
    data = blob.download_as_bytes()

    #infer schema
    dtype = {
        'outlet_id':str,
        'outlet_name':str,
        'outlet_address':str,
        'outlet_state':str,
        'postcode': str,  # Assuming postcode should be an integer
        'district': str,  # Assuming other_column should be a string
    # Add more columns and their data types as needed
    }
    df = pd.read_csv(io.BytesIO(data),dtype=dtype)
    # print(f'Pulled down file from bucket {bucket_name}, file name: {source_file_name}')
    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'

