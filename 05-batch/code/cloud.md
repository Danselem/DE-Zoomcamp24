## Running Spark in the Cloud

### Connecting to Google Cloud Storage 

Uploading data to GCS:

```bash
gsutil -m cp -r pq/ gs://dtc_data_lake_de-zoomcamp-nytaxi/pq

gsutil -m cp -r pq/ gs://mage-zoomcamp-dtc-de-412020/pq
```

Download the jar for connecting to GCS to any location (e.g. the `lib` folder):
`https://cloud.google.com/dataproc/docs/concepts/connectors/cloud-storage`
`mkdir lib
cd lib


```bash
gsutil cp gs://hadoop-lib/gcs/gcs-connector-hadoop3-2.2.5.jar
gsutil cp gs://hadoop-lib/gcs/gcs-connector-hadoop3-2.2.5.jar gcs-connector-hadoop3-2.2.5.jar
```

See the notebook with configuration in [09_spark_gcs.ipynb](09_spark_gcs.ipynb)

(Thanks Alvin Do for the instructions!)


### Local Cluster and Spark-Submit

Creating a stand-alone cluster ([docs](https://spark.apache.org/docs/latest/spark-standalone.html)):

```bash
cd /home/daniel/spark/spark-3.3.2-bin-hadoop3
./sbin/start-master.sh
```

Creating a worker:

```bash
URL="spark://de-zoomcamp.us-central1-a.c.dtc-de-412020.internal:7077"
./sbin/start-slave.sh ${URL}

URL="spark://de-zoomcamp.us-central1-a.c.dtc-de-412020.internal:7077"
./sbin/start-worker.sh ${URL}

./sbin/stop-worker.sh

# for newer versions of spark use that:
#./sbin/start-worker.sh ${URL}
```

Turn the notebook into a script:

```bash
jupyter nbconvert --to=script 06_spark_sql.ipynb
```

Edit the script and then run it:

```bash 
python 06_spark_sql.py \
    --input_green=data/pq/green/2020/*/ \
    --input_yellow=data/pq/yellow/2020/*/ \
    --output=data/report-2020
```

Use `spark-submit` for running the script on the cluster


export PYTHONPATH="${SPARK_HOME}/python/:$PYTHONPATH"
export PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH"

```bash
URL="URL="spark://de-zoomcamp.us-central1-a.c.dtc-de-412020.internal:7077"

spark-submit \
    --master="${URL}" \
    06_spark_sql.py \
        --input_green=data/pq/green/2021/*/ \
        --input_yellow=data/pq/yellow/2021/*/ \
        --output=data/report-2021
```

### Data Proc

Upload the script to GCS:

```bash
gsutil cp 06_spark_sql.py gs://mage-zoomcamp-dtc-de-412020/code/06_spark_sql.py
```

Params for the job:

* `--input_green=gs://mage-zoomcamp-dtc-de-412020/pq/green/2021/*/`
* `--input_yellow=gs://mage-zoomcamp-dtc-de-412020/pq/yellow/2021/*/`
* `--output=gs://mage-zoomcamp-dtc-de-412020/report-2021`


Using Google Cloud SDK for submitting to dataproc
([link](https://cloud.google.com/dataproc/docs/guides/submit-job#dataproc-submit-job-gcloud))

```bash
gcloud dataproc jobs submit pyspark \
    --cluster=de-zoomcamp-cluster \
    --region=us-central1 \
    gs://mage-zoomcamp-dtc-de-412020/code/06_spark_sql.py \
    -- \
        --input_green=gs://mage-zoomcamp-dtc-de-412020/pq/green/2020/*/ \
        --input_yellow=gs://mage-zoomcamp-dtc-de-412020/pq/yellow/2020/*/ \
        --output=gs://mage-zoomcamp-dtc-de-412020/report-2020
```

### Big Query

Upload the script to GCS:

```bash
gsutil cp 06_spark_sql_big_query.py gs://mage-zoomcamp-dtc-de-412020/code/06_spark_sql_big_query.py
gsutil rm gs://mage-zoomcamp-dtc-de-412020/code/06_spark_sql_big_query.py
```

Write results to big query ([docs](https://cloud.google.com/dataproc/docs/tutorials/bigquery-connector-spark-example#pyspark)):

```bash
gcloud dataproc jobs submit pyspark \
    --cluster=de-zoomcamp-cluster \
    --region=us-central1 \
    --jars=gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar \
    gs://mage-zoomcamp-dtc-de-412020/code/06_spark_sql_big_query.py \
    -- \
        --input_green=gs://mage-zoomcamp-dtc-de-412020/pq/green/2020/*/ \
        --input_yellow=gs://mage-zoomcamp-dtc-de-412020/pq/yellow/2020/*/ \
        --output=dtc-de-412020.trips_data_all.reports-2020
```

https://medium.com/towards-data-engineering/mastering-big-data-pipelines-harnessing-pyspark-in-google-cloud-platform-c42d6b02ff18


spark-shell --version

Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /___/ .__/\_,_/_/ /_/\_\   version 3.3.2
      /_/
                        
Using Scala version 2.12.15, OpenJDK 64-Bit Server VM, 11.0.2
Branch HEAD
Compiled by user liangchi on 2023-02-10T19:57:40Z
Revision 5103e00c4ce5fcc4264ca9c4df12295d42557af6
Url https://github.com/apache/spark
Type --help for more information.

```bash
gcloud dataproc jobs submit pyspark \
    --cluster=de-zoomcamp-cluster \
    --region=us-central1 \
    --jars=gs://spark-lib/bigquery/spark-3.3-bigquery-0.37.0.jar \
    gs://mage-zoomcamp-dtc-de-412020/code/06_spark_sql_big_query.py \
    -- \
        --input_green=gs://mage-zoomcamp-dtc-de-412020/pq/green/2020/*/ \
        --input_yellow=gs://mage-zoomcamp-dtc-de-412020/pq/yellow/2020/*/ \
        --output=dtc-de-412020.trips_data_all.reports-2020
```

