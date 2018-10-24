"""
A simple dag to read from ScyllaDB
"""
from airflow import DAG
from airflow.operators.bash_operator import PythonOperator
from datetime import datetime, timedelta

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


def print_context(ds, **kwargs):
    cluster = Cluster()
    session = cluster.connect('devices')
    rows = session.execute('SELECT deviceid, timestamp, data FROM devices ORDER BY timestamp DESC;')
    for device in rows:
        print(device.deviceid, device.timestamp, device.data)

    df = pd.DataFrame.from_dict(rows)

    # Initialize minioClient with an endpoint and access/secret keys.
    minioClient = Minio('minio:9000',
                        access_key='123456789',
                        secret_key='123456789',
                        secure=True)

    try:
        minioClient.make_bucket("data", location="us-east-1")
    except BucketAlreadyExists as err:
        pass
    except ResponseError as err:
        raise
    else:
        try:
            minioClient.put_object('data', 'pumaserver_debug.log', '/tmp/pumaserver_debug.log')
        except ResponseError as err:
            print(err)
    return 'Whatever you return gets printed in the logs'


run_this = PythonOperator(
    task_id='print_the_context',
    provide_context=True,
    python_callable=print_context,
    dag=dag)
