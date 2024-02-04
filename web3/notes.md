### To run Dockerfile

#### Build the image

```bash
docker build -t defi_ingest:v001 .
```

```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

start_date="01/01/2024 00:00:01"
end_date="29/01/2024 23:59:59"

`docker network ls`

docker run -it \
  --network=2_docker_sql_default \
  defi_ingest:v001 \
  --user=root \
  --password=root \
  --host=pgdatabase \
  --port=5432 \
  --db=ny_taxi \
  --table_name=defi_transactions \
  --start_date="${start_date}" \
  --end_date="${end_date}"
