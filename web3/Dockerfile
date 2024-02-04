FROM python:3.9.1

# RUN apt-get update && apt-get install wget

RUN pip install pandas pyarrow sqlalchemy deficrawler psycopg2-binary

WORKDIR /app

COPY defi-ingest.py defi-ingest.py 

ENTRYPOINT [ "python", "defi-ingest.py" ]