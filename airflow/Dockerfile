FROM continuumio/miniconda3:4.5.4

LABEL MAINTAINER barrachri

ARG AIRFLOW_VERSION=1.10.0
ARG AIRFLOW_HOME=/usr/local/airflow
ARG AIRFLOW_GPL_UNIDECODE=yes

ENV LANG C.UTF-8

RUN apt update && apt install -y  \
    build-essential \
    netcat

RUN conda install -c conda-forge -y numpy scikit-learn pandas pyarrow

RUN pip install --upgrade \
    pip \
    setuptools \
    wheel

RUN pip install \
    apache-airflow[postgres,jdbc]==$AIRFLOW_VERSION \
    minio==4.0.6 \
    cassandra-driver==3.15.1

RUN adduser --disabled-password --gecos airflow --home ${AIRFLOW_HOME} airflow

COPY src/scripts/entrypoint.sh /entrypoint.sh
COPY src/airflow.cfg ${AIRFLOW_HOME}/airflow.cfg

RUN chown -R airflow ${AIRFLOW_HOME}
RUN chown airflow: /entrypoint.sh
RUN chmod +x entrypoint.sh


EXPOSE 8080 5555 8793

USER airflow
WORKDIR ${AIRFLOW_HOME}

ENTRYPOINT ["/entrypoint.sh"]
CMD ["webserver"] # set default arg for entrypoint
