# Build a modern data infrastructure: Second part

## Agenda

    1. Build a Python producer & consumer (PRODUCER=>REDIS=>CONSUMER=>SCYLLA)
    2. Use Airflow to move things around
        1. Get things from Scylla and move them to parquet inside minio
    3. Use Airflow to train machine learning models
        1. Schedule training of models using parquet files maybe using mlflow
    4. What's next?
        1. Druid/Athena/Big Query/Yandex Click DB

## Tools that we are going to use

    Redis streams
    Scylla
    Airflow
    Docker
    Pandas and Parquet
    Minio
    Python ❤️

## Prerequisites

    If I say clone this repo locally and download these docker images you don't freak out
    A good knowledge of Python
    Python 3.6
    docker and docker compose