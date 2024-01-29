 -- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `de-zoomcamp-412301.ny_taxi.external_green_2022_tripdata` 
OPTIONS ( format = 'parquet',
    uris = ['gs://module-3-zoomcamp/green/green_tripdata_2022-*.parquet']);
    
-- Creating Materialized table
CREATE TABLE ny_taxi.green_taxi_2022 AS
SELECT * FROM de-zoomcamp-412301.ny_taxi.external_green_2022_tripdata;

-- Question 1: What is count of records for the 2022 Green Taxi Data??
SELECT COUNT(VendorID) FROM de-zoomcamp-412301.ny_taxi.green_taxi_2022;

--Question 2: Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.
--What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?

-- For External Table
SELECT COUNT(DISTINCT(PULocationID)) FROM de-zoomcamp-412301.ny_taxi.external_green_2022_tripdata;


-- For Materialized Table
SELECT COUNT(DISTINCT(PULocationID)) FROM de-zoomcamp-412301.ny_taxi.green_taxi_2022;

--Question 3: How many records have a fare_amount of 0?
SELECT COUNT(fare_amount) FROM de-zoomcamp-412301.ny_taxi.green_taxi_2022
WHERE fare_amount = 0;

-- Question 4-5
-- Creating a partition and cluster table
CREATE OR REPLACE TABLE de-zoomcamp-412301.ny_taxi.green_2022_tripdata_partitoned_clustered
PARTITION BY DATE(lpep_pickup_datetime)
CLUSTER BY PULocationID AS
SELECT * FROM de-zoomcamp-412301.ny_taxi.green_taxi_2022;


-- Scanning the partitioned_clustered table
SELECT DISTINCT(PULocationID)
FROM de-zoomcamp-412301.ny_taxi.green_2022_tripdata_partitoned_clustered
WHERE DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-06-30';

-- Scanning the non partitioned_clustered table
SELECT DISTINCT(PULocationID)
FROM de-zoomcamp-412301.ny_taxi.green_taxi_2022
WHERE DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-06-30';

-- Question 8
SELECT * FROM de-zoomcamp-412301.ny_taxi.green_taxi_2022;

SELECT * FROM de-zoomcamp-412301.ny_taxi.external_green_2022_tripdata;


