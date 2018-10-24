"""
A simple dag to read from ScyllaDB
"""
import logging
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from cassandra.cluster import Cluster
import pandas as pd
from minio import Minio
from minio.error import ResponseError, BucketAlreadyExists

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2018, 10, 22),
    'email': ['airflow@airflow.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'create_model', default_args=default_args, schedule_interval=timedelta(1))


def retrieve_data(ds, **kwargs):
    cluster = Cluster()
    session = cluster.connect('devices')
    rows = session.execute('SELECT deviceid, timestamp, data FROM devices;')

    for device in rows:
        logging.info(device.deviceid, device.timestamp, device.data)

run_this = PythonOperator(
    task_id='retrieve_data',
    provide_context=True,
    python_callable=retrieve_data,
    dag=dag)
