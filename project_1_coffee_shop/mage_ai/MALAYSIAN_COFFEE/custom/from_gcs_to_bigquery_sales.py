from google.cloud import bigquery
from google.oauth2 import service_account


if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

credentials_location = '/home/src/gcp_terraform.json'
project_id = 'de-zoomcamp-412301'
dataset_id = 'malaysian_coffee_chain'
table_id = 'sales'

credentials = service_account.Credentials.from_service_account_file(credentials_location)



@custom
def create_external_table_from_gcs(df):
    client = bigquery.Client(credentials=credentials)
    # Specify your custom logic here
    gcs_uri = [
        f"gs://malaysian_coffee_chain/processed/{table_id}/year=2018/*.parquet",
        f"gs://malaysian_coffee_chain/processed/{table_id}/year=2019/*.parquet",
        f"gs://malaysian_coffee_chain/processed/{table_id}/year=2020/*.parquet",
        f"gs://malaysian_coffee_chain/processed/{table_id}/year=2021/*.parquet",
        f"gs://malaysian_coffee_chain/processed/{table_id}/year=2022/*.parquet"
    ]

    table_ref = f"{project_id}.{dataset_id}.{table_id}"

    external_config = bigquery.ExternalConfig("PARQUET")
    external_config.source_uris = [gcs_uri]

    table = bigquery.Table(table_ref)
    table.external_data_configuration = external_config

    table = client.create_table(table, exists_ok=True)

    print(f"Table {table_id} created in dataset {dataset_id} of project {project_id}")


@test
def test_create_external_table():
    client = bigquery.Client(credentials=credentials, project=project_id)   
    for folder in folders:
        table_id = folder
        try:
            table = client.get_table(f"{project_id}.{dataset_id}.{table_id}")
            print(f"Table {table_id} exists in dataset {dataset_id}")
        except Exception as e:
            print(f"Failed to fetch table {table_id}. Error: {str(e)}")
            raise e  
