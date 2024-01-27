#!/usr/bin/env python

import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse
import os

    
def main(params):
  user = params.user
  password = params.password
  host = params.host
  port = params.port
  db = params.db
  table_name = params.table_name
  url = params.url

  # DOWNLOAD DATA

  if url.endswith('.csv.gz'):
    csv_name = 'output.csv.gz'
  else:
    csv_name = 'output.csv'

  os.system(f'wget {url} -O {csv_name}')
  
 
  # CREATE CONNECTION TO POSTGRES
  engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

  # READ THE TABLE 
  df_iter = pd.read_csv(csv_name,iterator=True,chunksize=100000)
  df = next(df_iter)

  # TRANSFORM DATETIME (yellow)
  # df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
  # df['tpep_pickup_datetime']=pd.to_datetime(df['tpep_pickup_datetime'])
  
# TRANSFORM DATETIME (green)
  df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])
  df['lpep_pickup_datetime']=pd.to_datetime(df['lpep_pickup_datetime'])

  # INSERT COLUMN TITLE 
  df.head(0).to_sql(name=table_name,con=engine, if_exists='replace')
  df.to_sql(name=table_name,con=engine, if_exists='append')

  while True:
    try: 
      start_time = time()
      df = next(df_iter)
      df.to_sql(name=table_name,con=engine, if_exists='append')
      end_time = time()
      print('Inserted another chunks, took %.3f seconds'%(end_time-start_time))

    except StopIteration:
      print("Finished ingestion into postgres database")
      break  


if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Ingestion pipeline in Docker')

  # Add a positional argument
  parser.add_argument('--user', help='user name for postgress',required=True)
  parser.add_argument('--password', help='password for postgress',required=True)
  parser.add_argument('--host', help='host for postgress',required=True)
  parser.add_argument('--port', help='port for postgress',required=True)
  parser.add_argument('--db', help='database for postgress',required=True)
  parser.add_argument('--table_name', help='table name where we will propagate our result to',required=True)
  parser.add_argument('--url', help='url of csv file',required=True)

  # Add an optional argument
  # parser.add_argument('--output', '-o', help='Path to the output file', default='output.txt')

  # Parse the command-line arguments
  args = parser.parse_args()

  main(args)