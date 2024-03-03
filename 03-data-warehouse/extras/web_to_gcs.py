import io
import os
import re
import requests
import pandas as pd
from google.cloud import storage

"""
Pre-reqs: 
1. `pip install pandas pyarrow google-cloud-storage`
2. Set GOOGLE_APPLICATION_CREDENTIALS to your project/service-account key
export GOOGLE_APPLICATION_CREDENTIALS='/home/daniel/.ssh/gcp-sv.json'
3. Set GCP_GCS_BUCKET as your bucket or change default value of BUCKET
"""

# services = ['fhv','green','yellow']
init_url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/'
# switch out the bucketname
BUCKET = os.environ.get("GCP_GCS_BUCKET", "mage-zoomcamp-dtc-de-412020")


def to_snake_case(column_name):
    # Use regex to identify consecutive uppercase characters
    snake_case_name = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', column_name)
    # Convert to lowercase and replace consecutive underscores
    return snake_case_name.lower().replace('__', '_')

def columns_to_snake_case(df):
    df.columns = [to_snake_case(col) for col in df.columns]

def upload_to_gcs(bucket, object_name, local_file):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    """
    # # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # # (Ref: https://github.com/googleapis/python-storage/issues/74)
    # storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    # storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB

    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)


def web_to_gcs(year, service):
    for i in range(12):
        
        # sets the month part of the file_name string
        month = '0'+str(i+1)
        month = month[-2:]

        # csv file_name
        file_name = f"{service}_tripdata_{year}-{month}.csv.gz"

        # download it using requests via a pandas df
        request_url = f"{init_url}{service}/{file_name}"
        r = requests.get(request_url)
        open(file_name, 'wb').write(r.content)
        print(f"Local: {file_name}")

        # read it back into a parquet file
        if service == 'fhv':
            df = pd.read_csv(file_name, compression='gzip', low_memory=False, encoding='latin1')
            
            columns_to_snake_case(df)
            
            if 'drop_off_datetime' in df.columns:
                # Rename 'dropOff_datetime' to 'dropoff_datetime'
                df.rename(columns={'drop_off_datetime': 'dropoff_datetime'}, inplace=True)
    
            # Check if 'dropoff_datetime' column exists
            elif 'dropoff_datetime' in df.columns:
                # Do nothing, the column name is already correct
                pass
            
            df["dispatching_base_num"] = df["dispatching_base_num"].astype('string')
            df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"])
            df["dropoff_datetime"] = pd.to_datetime(df["dropoff_datetime"])
            df["pulocation_id"] = df["pulocation_id"].astype('Int64')
            df["dolocation_id"] = df["dolocation_id"].astype('Int64')
            df["sr_flag"] = df["sr_flag"].astype('Int64')
            df["affiliated_base_number"] = df["affiliated_base_number"].astype('string')
            

            file_name = file_name.replace('.csv.gz', '.parquet')
            os.system("rm *.csv.gz")
            df.to_parquet(file_name, engine='pyarrow')
            print(f"Parquet: {file_name}")

            # upload it to gcs 
            upload_to_gcs(BUCKET, f"{service}/{file_name}", file_name)
            print(f"GCS: {service}/{file_name}")
            os.system("rm *.parquet")
            
        elif service == 'yellow':
            df = pd.read_csv(file_name, compression='gzip', low_memory=False, encoding='latin1')

            columns_to_snake_case(df)

            df = df.astype({'vendor_id':'Int64','passenger_count':'float', 'pulocation_id': 'Int64',
                            'dolocation_id': 'Int64', 'trip_distance': 'float',
                            'ratecode_id': 'Int64', 'store_and_fwd_flag': 'string',
                            'payment_type': 'Int64', 'fare_amount': 'float',
                            'extra': 'float', 'mta_tax': 'float', 'tip_amount': 'float', 
                            'tolls_amount': 'float', 'improvement_surcharge': 'float', 
                            'total_amount': 'float', 'congestion_surcharge': 'float'})
            
            df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
            df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])
            
            file_name = file_name.replace('.csv.gz', '.parquet')
            os.system("rm *.csv.gz")
            df.to_parquet(file_name, engine='pyarrow')
            print(f"Parquet: {file_name}")

            # upload it to gcs 
            upload_to_gcs(BUCKET, f"{service}/{file_name}", file_name)
            print(f"GCS: {service}/{file_name}")
            os.system("rm *.parquet")
            
            
        else:
            # load green data
            df = pd.read_csv(file_name, compression='gzip', low_memory=False, encoding='latin1')
            
            columns_to_snake_case(df)     
            
            df = df.astype({'vendor_id':'Int64','passenger_count':'float', 'pulocation_id': 'Int64',
                            'dolocation_id': 'Int64', 'trip_distance': 'float',
                            'ratecode_id': 'Int64', 'store_and_fwd_flag': 'string',
                            'payment_type': 'Int64', 'fare_amount': 'float',
                            'extra': 'float', 'mta_tax': 'float', 'tip_amount': 'float', 
                            'tolls_amount': 'float', 'improvement_surcharge': 'float', 
                            'total_amount': 'float', 'congestion_surcharge': 'float',
                            'ehail_fee': 'float', 'trip_type': 'float'})
            
            df["lpep_pickup_datetime"] = pd.to_datetime(df["lpep_pickup_datetime"])
            df["lpep_dropoff_datetime"] = pd.to_datetime(df["lpep_dropoff_datetime"])
            

            file_name = file_name.replace('.csv.gz', '.parquet')
            os.system("rm *.csv.gz")
            df.to_parquet(file_name, engine='pyarrow')
            print(f"Parquet: {file_name}")

            # upload it to gcs 
            upload_to_gcs(BUCKET, f"{service}/{file_name}", file_name)
            print(f"GCS: {service}/{file_name}")
            os.system("rm *.parquet")


web_to_gcs('2019', 'green')
web_to_gcs('2020', 'green')
web_to_gcs('2019', 'yellow')
web_to_gcs('2020', 'yellow')
web_to_gcs('2019', 'fhv')
web_to_gcs('2020', 'fhv')