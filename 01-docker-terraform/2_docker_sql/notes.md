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