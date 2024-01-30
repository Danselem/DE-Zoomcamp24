FROM python:3.10.1-slim

RUN apt-get install wget

RUN pip install pandas sqlalchemy deficrawler DeFiLlama-Curl psycopg2-binary

WORKDIR /app

COPY ingest_data.py ingest_data.py 

ENTRYPOINT [ "python", "ingest_data.py" ]