
--Question 1--
--Create a materialized view to compute the average, min and max trip time between each taxi zone.--
--From this MV, find the pair of taxi zones with the highest average trip time-
--You may need to use the dynamic filter pattern for this-- 

CREATE MATERIALIZED VIEW taxi_trips_stats AS
SELECT
  tz1.zone AS pickup_zone,
  tz2.zone AS dropoff_zone,
  AVG(td.tpep_dropoff_datetime-td.tpep_pickup_datetime) AS avg_trip_time,
  MIN(td.tpep_dropoff_datetime-td.tpep_pickup_datetime) AS min_trip_time,
  MAX(td.tpep_dropoff_datetime-td.tpep_pickup_datetime) AS max_trip_time
FROM  
  trip_data td 
JOIN
  taxi_zone tz1 ON td.pulocationid = tz1.location_id
JOIN
  taxi_zone tz2 ON td.dolocationid = tz2.location_id
GROUP BY
  tz1.zone, tz2.zone;

SELECT
  pickup_zone,
  dropoff_zone,
  avg_trip_time
FROM 
  taxi_trips_stats
ORDER BY
  avg_trip_time DESC
LIMIT 1;


--Question 2--
--Recreate the MV(s) in question 1, to also find the number of trips for the pair of taxi zones with the highest average trip time--


CREATE MATERIALIZED VIEW taxi_trips_count AS
SELECT
  tz1.zone AS pickup_zone,
  tz2.zone AS dropoff_zone,
  COUNT(*) as number_trips,
  AVG(td.tpep_dropoff_datetime-td.tpep_pickup_datetime) AS avg_trip_time,
  MIN(td.tpep_dropoff_datetime-td.tpep_pickup_datetime) AS min_trip_time,
  MAX(td.tpep_dropoff_datetime-td.tpep_pickup_datetime) AS max_trip_time
FROM  
  trip_data td 
JOIN
  taxi_zone tz1 ON td.pulocationid = tz1.location_id
JOIN
  taxi_zone tz2 ON td.dolocationid = tz2.location_id
GROUP BY
  tz1.zone, tz2.zone;


SELECT
  number_trips,
  pickup_zone,
  dropoff_zone
FROM 
  taxi_trips_count
ORDER BY  
  avg_trip_time DESC
LIMIT 1;


--query some info to check the answer--
--query the time difference for each record and get the highest time spent--

with t as (
  SELECT
    tz1.zone AS pickup_zone,
    tz2.zone AS dropoff_zone,
    td.tpep_dropoff_datetime-td.tpep_pickup_datetime AS trip_diffference
  FROM  
    trip_data td 
  JOIN
    taxi_zone tz1 ON td.pulocationid = tz1.location_id
  JOIN
    taxi_zone tz2 ON td.dolocationid = tz2.location_id
)
SELECT 
  pickup_zone,
  dropoff_zone,
  trip_diffference
FROM
  t
ORDER BY
  trip_diffference DESC
LIMIT 5;

--it return 'Queensbridge/Ravenswood', so we check on this and there is 39 trips bring down its maximum time--

SELECT *
FROM taxi_trips_count
WHERE "pickup_zone" = 'Queensbridge/Ravenswood';

--Question 3--
--From the latest pickup time to 17 hours before, what are the top 3 busiest zones in terms of number of pickups?--
-- CREATE MATERIALIZED VIEW top_busiest_pickup_zone AS
SELECT 
  tz.zone as pickup_zone,
  count(*) as number_trips
FROM 
  trip_data td
JOIN 
  taxi_zone tz ON td.pulocationid = tz.location_id
WHERE 
  td.tpep_pickup_datetime >= (SELECT MAX(tpep_pickup_datetime)-interval '17 hours' FROM trip_data)
  AND
  td.tpep_pickup_datetime <= (SELECT MAX(tpep_pickup_datetime) FROM trip_data)
GROUP BY
  pickup_zone
ORDER BY
  number_trips DESC
LIMIT 3;


