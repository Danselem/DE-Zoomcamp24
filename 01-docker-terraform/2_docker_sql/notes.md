### Docker
`docker network create pg-network`

`docker volume create --name dtc_postgres_volume_local -d local`
### Postgres
```
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v dtc_postgres_volume_local:/var/lib/postgresql/data \
    -p 5432:5432 \
    --network pg-network \
    --name pg-database \
    postgres:13
```

### pgAdmin
```
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4
```

### How to view docker images
`docker images`

### How to delete images
`docker rmi -f $(docker images -q)`

### How to stop containers
` docker stop $(docker ps -a -q)`

### How to delete containers
`docker rm $(docker ps -a -q)`

### On pgAdmin
Register, General, 
Name: MyServer
Connection
Host name: pg-database
port: 5432
maintenance database: postgres
username: root
password: root


### Data 
`https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz`
`gunzip yellow_tripdata_2021-01.csv.gz`


### To view available container
`docker ps -a`

### To start a container
`docker start <CONTAINER ID>`



### To run Dockerfile

#### Build the image

```bash
docker build -t taxi_ingest:v001 .
```

#### Run the script with Docker

```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

docker run -it \
  --network=pg-network \
  taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=${URL}
```



docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=pg-network \
  --name pg-database \
  postgres:13



### docker compose
`docker compose up -d`

### To run Dockerfile

#### Build the image

```bash
docker build -t taxi_ingest:v001 .
```

```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

`docker network ls`

docker run -it \
  --network=2_docker_sql_default \
  taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pgdatabase \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=${URL}



### pgcli
sudo apt install pgcli
`pgcli -h localhost -U root -d ny_taxi`


### Assignment

`docker build -t green_ingest:v001 .`


URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz"

docker run -it \
  --network=2_docker_sql_default \
  green_ingest:v001 \
    --user=root \
    --password=root \
    --host=pgdatabase \
    --port=5432 \
    --db=ny_taxi \
    --table_name=green_taxi_trips \
    --url=${URL}



### SQL
`
SELECT
  *
FROM
  yellow_taxi_trips t,
  zones zpu,
  zones zdo
WHERE
  t."PULocationID" = zpu."LocationID" AND
  t."DOLocationID" = zdo."LocationID"
LIMIT 100;
`

`
-- Joining yellow taxi trips and zones data
SELECT
  tpep_pickup_datetime, 
  tpep_dropoff_datetime,
  total_amount,
  CONCAT(zpu."Borough", ' /', zpu."Zone") AS "pickup_loc",
  CONCAT(zdo."Borough", ' /', zdo."Zone") AS "dropoff_loc"
FROM
  yellow_taxi_trips t,
  zones zpu,
  zones zdo
WHERE
  t."PULocationID" = zpu."LocationID" AND
  t."DOLocationID" = zdo."LocationID"
LIMIT 100;
`


```
SELECT
  tpep_pickup_datetime, 
  tpep_dropoff_datetime,
  total_amount,
  CONCAT(zpu."Borough", ' /', zpu."Zone") AS "pickup_loc",
  CONCAT(zdo."Borough", ' /', zdo."Zone") AS "dropoff_loc"
FROM
  yellow_taxi_trips t JOIN zones zpu
    ON t."PULocationID" = zpu."LocationID"
  JOIN zones zdo
    ON t."DOLocationID" = zdo."LocationID"
LIMIT 100;
```

```
SELECT
  tpep_pickup_datetime, 
  tpep_dropoff_datetime,
  total_amount,
  "PULocationID",
  "DOLocationID"
FROM
  yellow_taxi_trips t
WHERE
  "PULocationID" = NULL
LIMIT 100
```

```
SELECT
  tpep_pickup_datetime, 
  tpep_dropoff_datetime,
  total_amount,
  "PULocationID",
  "DOLocationID"
FROM
  yellow_taxi_trips t
WHERE
  "PULocationID" NOT IN (SELECT "LocationID" FROM zones)
LIMIT 100
```

```
SELECT
  tpep_pickup_datetime, 
  tpep_dropoff_datetime,
  total_amount,
  "PULocationID",
  "DOLocationID"
FROM
  yellow_taxi_trips t LEFT JOIN zones zpu
    ON t."PULocationID" = zpu."LocationID"
  LEFT JOIN zones zdo
    ON t."DOLocationID" = zdo."LocationID"
LIMIT 100
```

```
SELECT
  tpep_pickup_datetime, 
  tpep_dropoff_datetime,
  total_amount,
  "PULocationID",
  "DOLocationID"
FROM
  yellow_taxi_trips t OUTER JOIN zones zpu
    ON t."PULocationID" = zpu."LocationID"
  LEFT JOIN zones zdo
    ON t."DOLocationID" = zdo."LocationID"
LIMIT 100
```