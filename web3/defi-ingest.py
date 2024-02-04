#!/usr/bin/env python
# coding: utf-8

import os
import argparse

from time import time

import pandas as pd
from sqlalchemy import create_engine

from deficrawler import Oracle
from deficrawler import Dex
from deficrawler import Lending

def main(params):
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    table_name = params.table_name
    start_date = params.start_date
    end_date = params.end_date
    
    csv_name = 'defi-data.csv'
    
    # Lending protocols
    aave = Lending(protocol="Aave", chain="Ethereum", version=2)
    aave_polygon = Lending(protocol="Aave", chain="Polygon", version=2)
    compound = Lending(protocol="Compound", chain="Ethereum", version=2)
    cream = Lending(protocol="Cream", chain="Ethereum", version=2)
    cream_bsc = Lending(protocol="Cream", chain="bsc", version=2)
    cream_poly = Lending(protocol="Cream", chain="Polygon", version=2)
    cream_ether = Lending(protocol="Cream", chain="Ethereum", version=2)
    
    
    list_borrows = [*aave.get_data_from_date_range(start_date, end_date, "borrow"),
                *aave_polygon.get_data_from_date_range(start_date, end_date, "borrow"),
                *compound.get_data_from_date_range(start_date, end_date, "borrow"),
                *cream_bsc.get_data_from_date_range(start_date, end_date, "borrow"),
                *cream_poly.get_data_from_date_range(start_date, end_date, "borrow"),
                *cream.get_data_from_date_range(start_date, end_date, "borrow"),
                *cream_ether.get_data_from_date_range(start_date, end_date, "borrow")]
    
    df_borrows = pd.DataFrame.from_records(list_borrows)
    df_borrows.to_csv(csv_name, index=False)
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=30000)
    
    df = next(df_iter)

    df['time'] = pd.to_datetime(df_borrows['timestamp'],unit='s')

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    df.to_sql(name=table_name, con=engine, if_exists='append')


    while True: 

        try:
            t_start = time()
            
            df = next(df_iter)

            df['time'] = pd.to_datetime(df_borrows['timestamp'],unit='s')

            df.to_sql(name=table_name, con=engine, if_exists='append')

            t_end = time()

            print('inserted another chunk, took %.3f second' % (t_end - t_start))

        except StopIteration:
            print("Finished ingesting data into the postgres database")
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name', required=True, help='name of the table where we will write the results to')
    parser.add_argument('--start_date', required=True, help='start date for the transaction')
    parser.add_argument('--end_date', required=True, help='end date of transactions')

    args = parser.parse_args()

    main(args)