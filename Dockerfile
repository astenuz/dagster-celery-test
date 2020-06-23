FROM python:3.8-slim

# Cron is required to use scheduling in Dagster
RUN apt-get update && apt-get install -yqq cron && pip install pipenv

RUN mkdir -p /opt/dagster/home /opt/dagster/app

COPY Pipfile Pipfile.lock /opt/dagster/app/

# Copy your pipeline code and entrypoint.sh to /opt/dagster/app
COPY app/* /opt/dagster/app/

# Copy dagster instance YAML to $DAGSTER_HOME
COPY home/* /opt/dagster/home/

WORKDIR /opt/dagster/app

RUN pipenv install && chmod +x run.sh && chmod +x worker.sh

EXPOSE 2001

ENTRYPOINT ["/opt/dagster/app/run.sh"]