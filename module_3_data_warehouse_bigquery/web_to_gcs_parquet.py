import os
# import requests
import pandas as pd
from google.cloud import storage
import pyarrow as pa
import pyarrow.parquet as pq


# services = ['fhv','green','yellow']
init_url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/'
# switch out the bucketname
BUCKET = os.environ.get("GCP_GCS_BUCKET")


def upload_to_gcs(bucket, object_name, parquet_binary):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    """
    # # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # # (Ref: https://github.com/googleapis/python-storage/issues/74)
    # storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    # storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB

    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)
    blob.upload_from_string(parquet_binary.getvalue().to_pybytes(), content_type='application/octet-stream')



def web_to_gcs_parquet(year,service):
   
   for i in range(12): 
      # sets the month part of the file_name string
      month = '0'+str(i+1)
      month = month[-2:]

      # csv file_name
      file_name = f"{service}_tripdata_{year}-{month}.csv.gz"

      # adjust the url name
      request_url = f"{init_url}{service}/{file_name}"

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
      
      # # parse the date column
      if service == 'yellow':
        parse_dates = ['tpep_pickup_datetime','tpep_dropoff_datetime']
      else:
        parse_dates = ['lpep_pickup_datetime','lpep_dropoff_datetime']

      # read it into dataframe directly from pandas
      print(f"--------------------------Acessing Raw File: {file_name}---------------------------")

      df = pd.read_csv(request_url, compression='gzip',dtype=taxi_dtypes)

      print(f"--------------------------Acessed Raw File: {file_name}---------------------------")

      # change it from pandas to parquet
      print("--------------------------Changing to .parquet---------------------------")

      file_name = file_name.replace('.csv.gz', '.parquet')

      
      # Convert DataFrame to Parquet format in-memory
      parquet_binary = pa.BufferOutputStream()
      pq.write_table(pa.Table.from_pandas(df), parquet_binary)
          

      print(f"--------------------------Changed format to Parquet: {file_name}-----------------------")

      # write to GCS
      print("--------------------------Uploading to GCS----------------------------------------------")
      # pq.write_to_dataset(
      #     table,
      #     root_path=f"{BUCKET}/{service}/{file_name}",
      #     filesystem=gcs
      # )

      # upload it to gcs 
      upload_to_gcs(BUCKET, f"{service}/{file_name}", parquet_binary)
      print(f"GCS: {service}/{file_name}")
      # print(f"GCS: {BUCKET}/{service}/{file_name}")


web_to_gcs_parquet(year='2022',service='green')

