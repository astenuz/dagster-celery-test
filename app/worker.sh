#!/bin/sh
export DAGSTER_HOME=/opt/dagster/home

# Launch Dagit as a service
DAGSTER_HOME=/opt/dagster/home pipenv run dagster-celery worker start -y /opt/dagster/home/celery_execution.yaml