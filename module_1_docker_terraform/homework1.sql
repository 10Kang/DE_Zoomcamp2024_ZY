-- Question 3

SELECT 
	COUNT(1) AS "Trips"
FROM
	green_taxi_trips t
WHERE DATE(t."lpep_pickup_datetime")= '2019-09-18'
AND DATE(t."lpep_dropoff_datetime")= '2019-09-18';

-- Question 4

SELECT
	trip_distance,
	CAST(t."lpep_pickup_datetime" AS DATE) as "pick_up_day"
FROM 
	green_taxi_trips t
ORDER BY
	t."trip_distance" DESC;

-- Question 5

SELECT
	zpu."Borough" as "place",
	SUM(total_amount) as "COUNT"
FROM 
	green_taxi_trips t LEFT JOIN zones zpu
	ON t."PULocationID" = zpu."LocationID" 

WHERE DATE(t."lpep_pickup_datetime")= '2019-09-18'
AND DATE(t."lpep_dropoff_datetime")= '2019-09-18'

GROUP BY
	zpu."Borough"
LIMIT 100;

-- Question 6

SELECT 
	t."tip_amount",
	zdo."Zone"
FROM 
	green_taxi_trips t JOIN zones zpu
	ON t."PULocationID" = zpu."LocationID"
	JOIN zones zdo 
	ON t."DOLocationID" = zdo."LocationID" 
WHERE
	zpu."Zone" = 'Astoria'
ORDER BY
	t."tip_amount" DESC;