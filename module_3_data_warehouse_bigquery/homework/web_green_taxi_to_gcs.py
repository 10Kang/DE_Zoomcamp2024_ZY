
import os
import requests
import pandas as pd
from google.cloud import storage
import pyarrow.parquet as pq
from io import BytesIO


# services = ['fhv','green','yellow']
init_url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/'
# switch out the bucketname
bucket_name = os.environ.get("GCP_GCS_BUCKET")



def upload_to_gcs(bucket_name, destination_blob_name, parquet_file):
  
  # Upload Arrow Table to GCS as Parquet file
  client = storage.Client()
  bucket = client.get_bucket(bucket_name)
  blob = bucket.blob(destination_blob_name)
  with BytesIO() as buffer:
      pq.write_table(parquet_file, buffer)
      buffer.seek(0)
      blob.upload_from_file(buffer, content_type='application/octet-stream')



def url_to_gcs_parquet(year, service):
    
    # for 12 month
    for i in range(12):
        # sets the month part of the file_name string
        month = '0'+str(i+1)
        month = month[-2:]

        # parquet file_name
        file_name = f"{service}_tripdata_{year}-{month}.parquet"
        # parquet_url
        parquet_url =  f"{init_url}{file_name}"

        print('Getting data from',parquet_url)
        # Read Parquet file from URL using pyarrow
        response = requests.get(parquet_url)
        parquet_data = BytesIO(response.content)
        parquet_file = pq.read_table(parquet_data)

        # upload it to gcs 
        upload_to_gcs(bucket_name, f"{service}/{file_name}", parquet_file)
        print(f"Parquet file uploaded to GCS: gs://{bucket_name}/{service}/{file_name}")



# web_to_gcs('2019', 'green')
# web_to_gcs('2020', 'green')
url_to_gcs_parquet('2022', 'green')
