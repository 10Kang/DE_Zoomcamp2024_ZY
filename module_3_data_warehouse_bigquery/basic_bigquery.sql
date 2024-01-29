 -- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `de-zoomcamp-412301.ny_taxi.external_yellow_tripdata` 
OPTIONS ( format = 'parquet',
    uris = ['gs://module-3-zoomcamp/yellow/yellow_tripdata_2020-*.parquet',
    'gs://module-3-zoomcamp/yellow/yellow_tripdata_2019-*.parquet']);


-- change the datetime to TIMESTAMP
CREATE OR REPLACE TABLE de-zoomcamp-412301.ny_taxi.external_yellow_tripdata_corrected AS
SELECT *, PARSE_DATETIME('%Y-%m-%d %H:%M:%S', tpep_pickup_datetime) AS pickup_date 
FROM de-zoomcamp-412301.ny_taxi.external_yellow_tripdata;

-- select 10 rows to see 
SELECT * FROM `ny_taxi.external_yellow_tripdata_corrected` 
ORDER BY pickup_date ASC
LIMIT 500 ;


-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE de-zoomcamp-412301.ny_taxi.yellow_tripdata_non_partitoned AS
SELECT * FROM de-zoomcamp-412301.ny_taxi.external_yellow_tripdata_corrected;

-- Create a partitioned table from external table
CREATE OR REPLACE TABLE de-zoomcamp-412301.ny_taxi.yellow_tripdata_partitoned
PARTITION BY
  DATE(pickup_date) AS
SELECT * FROM de-zoomcamp-412301.ny_taxi.external_yellow_tripdata_corrected;

-- Impact of partition
-- Scanning 1.6GB of data
SELECT DISTINCT(VendorID)
FROM de-zoomcamp-412301.ny_taxi.yellow_tripdata_non_partitoned
WHERE DATE(pickup_date) BETWEEN '2019-06-01' AND '2019-06-30';

-- Scanning ~106 MB of DATA
SELECT DISTINCT(VendorID)
FROM de-zoomcamp-412301.ny_taxi.yellow_tripdata_partitoned
WHERE DATE(pickup_date) BETWEEN '2019-06-01' AND '2019-06-30';


-- Let's look into the partitons
SELECT table_name, partition_id, total_rows
FROM `ny_taxi.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = 'yellow_tripdata_partitoned'
ORDER BY total_rows DESC;

-- Creating a partition and cluster table
CREATE OR REPLACE TABLE de-zoomcamp-412301.ny_taxi.yellow_tripdata_partitoned_clustered
PARTITION BY DATE(pickup_date)
CLUSTER BY VendorID AS
SELECT * FROM de-zoomcamp-412301.ny_taxi.external_yellow_tripdata_corrected;

-- Query scans 1.1 GB
SELECT count(*) as trips
FROM de-zoomcamp-412301.ny_taxi.yellow_tripdata_partitoned
WHERE DATE(pickup_date) BETWEEN '2019-06-01' AND '2020-12-31'
  AND VendorID=1;


-- Query scans 864.5 MB
SELECT count(*) as trips
FROM de-zoomcamp-412301.ny_taxi.yellow_tripdata_partitoned_clustered
WHERE DATE(pickup_date) BETWEEN '2019-06-01' AND '2020-12-31'
  AND VendorID=1;
