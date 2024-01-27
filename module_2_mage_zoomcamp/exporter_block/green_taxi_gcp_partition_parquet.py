from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
import pyarrow as pa
import pyarrow.parquet as pq
import os
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

# set credential
os.environ['GOOGLE_APPLICATION_CREDENTIALS']="/home/src/de-zoomcamp-412301-edd017044193.json"
bucket_name = "mage-zoomcamp-zy"
project_id = "de-zoomcamp-412301"

table_name = "nyc_taxi_data"

root_path = f'{bucket_name}/{table_name}'

@data_exporter
def export_data(data, *args, **kwargs):
    """
    Exports data to some source.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """

    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'dev'

    # throw into pyarrow
    table = pa.Table.from_pandas(data)

    # get the filesystem
    gcs = pa.fs.GcsFileSystem()

    # write to GCS
    pq.write_to_dataset(
        table,
        root_path=root_path,
        partition_cols=['lpep_pickup_date'],
        filesystem=gcs
    )