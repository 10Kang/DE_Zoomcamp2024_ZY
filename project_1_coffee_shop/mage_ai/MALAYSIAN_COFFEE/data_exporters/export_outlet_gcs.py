import pandas as pd
from google.cloud import storage
import os
import io
from google.oauth2 import service_account

credentials_location = '/home/src/gcp_terraform.json'
credentials = service_account.Credentials.from_service_account_file(credentials_location)


if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
# def export_data_to_google_cloud_storage(df: DataFrame, **kwargs) -> None:
#     """
#     Template for exporting data to a Google Cloud Storage bucket.
#     Specify your configuration settings in 'io_config.yaml'.

#     Docs: https://docs.mage.ai/design/data-loading#googlecloudstorage
#     """
#     config_path = path.join(get_repo_path(), 'io_config.yaml')
#     config_profile = 'default'

#     bucket_name = 'malaysian_coffee_chain'
#     object_key = 'processed/outlet/outlet.csv'

#     GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).export(
#         df,
#         bucket_name,
#         object_key,
#     )

def df_to_gcp_csv(df):
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket('malaysian_coffee_chain')
    blob = bucket.blob('processed/outlet/outlet.csv')
    blob.upload_from_string(df.to_csv(index=False), 'text/csv')
    # print(f'DataFrame uploaded to bucket {dest_bucket_name}, file name: {dest_file_name}')

