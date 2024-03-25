import json
import time 
from kafka import KafkaProducer
import pandas as pd


# initiate the KafkaProducer

server = 'localhost:9092'

producer = KafkaProducer(
    bootstrap_servers=[server]
)

# define the topic to be published
topic = 'green-trips'

# read the dataframe 
# define the data types for each column
dtype_dict = {
    'lpep_pickup_datetime': 'str',
    'lpep_dropoff_datetime': 'str',
    'PULocationID': 'int',
    'DOLocationID': 'int',
    'passenger_count': 'float',
    'trip_distance': 'float',
    'tip_amount': 'float'
}

# define the columns you want to keep
columns_to_keep = [
    'lpep_pickup_datetime',
    'lpep_dropoff_datetime',
    'PULocationID',
    'DOLocationID',
    'passenger_count',
    'trip_distance',
    'tip_amount'
]

# read the csv file
df_green = pd.read_csv('green_tripdata_2019-10.csv', usecols=columns_to_keep, dtype=dtype_dict, na_values=[''])

# fill the missing value with zero
df_green['passenger_count'] = df_green['passenger_count'].fillna(0).astype(int)


# Record the start time
start_time = time.time()

# publishing data 

for row in df_green.itertuples(index=False):
    row_dict = {col: getattr(row, col) for col in row._fields}
    
    # Filter the dictionary to keep only the specified columns
    row_dict_filtered = {key: value for key, value in row_dict.items() if key in columns_to_keep}
    
    # Convert the dictionary to JSON and encode as bytes
    message = pd.Series(row_dict_filtered).to_json().encode('utf-8')
    
    # Send the message to the Kafka topic
    producer.send(topic, value=message)

    # print message to know which message is sent
    print(row_dict_filtered)
   
# close the producer
producer.close()

# record the time ended
end_time = time.time()

# calculate execution time
time_used = end_time - start_time

# print the execution time
print(f'Total used time{time_used:.2f} seconds.')