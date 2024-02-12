-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `dtc-de-412020.ny_taxi.external_green22_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://mage-zoomcamp-dtc-de-412020/ny_taxi/green_taxi_data_2022.parquet']
);

-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE dtc-de-412020.ny_taxi.green22_tripdata AS
SELECT * FROM dtc-de-412020.ny_taxi.external_green22_tripdata;

-- Check green22 trip data
SELECT * FROM dtc-de-412020.ny_taxi.external_green22_tripdata limit 10;

-- Check number ofgreen22 trip data
SELECT COUNT(1) FROM dtc-de-412020.ny_taxi.external_green22_tripdata;


-- Scanning 0 MB of DATA
SELECT DISTINCT(pulocation_id)
FROM dtc-de-412020.ny_taxi.external_green22_tripdata;

-- Scanning 6.41 MB of DATA
SELECT DISTINCT(pulocation_id)
FROM dtc-de-412020.ny_taxi.green22_tripdata;

-- How many records have a fare_amount of 0?
SELECT COUNT(1)
FROM dtc-de-412020.ny_taxi.green22_tripdata
WHERE fare_amount = 0;

-- Creating a partition and cluster table
CREATE OR REPLACE TABLE dtc-de-412020.ny_taxi.green22_tripdata_partitoned_clustered
PARTITION BY lpep_pickup_datetime
CLUSTER BY pulocation_id AS
SELECT * FROM dtc-de-412020.ny_taxi.green22_tripdata;


-- Query scans 12.82 MB
SELECT DISTINCT(pulocation_id)
FROM dtc-de-412020.ny_taxi.green22_tripdata
WHERE lpep_pickup_datetime BETWEEN '2022-06-01' AND '2022-06-30';

-- Query scans 1.12 MB
SELECT DISTINCT(pulocation_id)
FROM dtc-de-412020.ny_taxi.green22_tripdata_partitoned_clustered
WHERE lpep_pickup_datetime BETWEEN '2022-06-01' AND '2022-06-30';
