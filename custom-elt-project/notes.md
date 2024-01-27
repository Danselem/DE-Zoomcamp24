### Creating the Docker Image

`docker-compose up -d`

`docker ps`
```bash
24b914aee03f   postgres:latest   "docker-entrypoint.s…"   12 minutes ago   Up 12 minutes   0.0.0.0:5434->5432/tcp, :::5434->5432/tcp   custom-elt-project_destination_postgres_1
e8530538169c   postgres:latest   "docker-entrypoint.s…"   12 minutes ago   Up 12 minutes   0.0.0.0:5433->5432/tcp, :::5433->5432/tcp   custom-elt-project_source_postgres_1
```

`docker exec -it custom-elt-project_destination_postgres_1 psql -U postgres`

### Connect to the DB

`\c destination_db`