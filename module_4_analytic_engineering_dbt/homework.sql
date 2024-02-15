 -- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `de-zoomcamp-412301.trips_data_all.external_fhv_tripdata` 
OPTIONS ( format = 'csv',
    uris = ['gs://module-4-zoomcamp-homework/fhv/*csv']);


-- Create a materialized table 
CREATE TABLE trips_data_all.fhv_tripdata AS
SELECT *
FROM trips_data_all.external_fhv_tripdata;

-- Query some of the information
SELECT COUNT(pickup_datetime) FROM `trips_data_all.fhv_tripdata`;

-- Query answer for Question 3
SELECT COUNT(pickup_datetime) FROM `production.fact_fhv_trips`;