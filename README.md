# Dagster with celery and docker

This is an example of a simple parallel pipeline packaged in docker that runs with celery through a simple `docker-compose up` command. It uses:

- docker to deploy database, rabbitmq, dagster-dagit and dagster-celery workers
- celery as execution backend
- s3 as intermediate storage backend

This example is meant to illustrate how the components in a simple scalable dagster deployment are connected and configured. For instance, one particular aspect that is a little untouched in the documentation is how to use a custom broker connection string and what could be the contents of the yaml passed to the `dagster-celery` worker initialization. 

## Run example

Prerequisites:
- s3 bucket and an account with write and read permissions on the bucket

Steps:

- setup the aws s3 environment variables of the account, these are used in the docker-compose and passed to the dagster instances

    - `AWS_ACCESS_KEY_ID`
    - `AWS_SECRET_ACCESS_KEY`
    - `AWS_DEFAULT_REGION`
    
- change the configuration file in `app/celery_execution.yaml` to the appropriate bucket name

3) build the image with

```shell script
$ docker build . -t dagster_test
```
The code is copied directly into the image

- then deploy the nodes with docker-compose

```shell script
$ docker-compose up
```

There could be some issues with rabbitmq. In theory, the configuration inside `.docker/rabbitmq/etc/rabbitmq.conf` should create a vhost called `dagster` that could be accesed with credentials `rabbitmq:rabbitmq`(`user:pass`). If this is not the case access the web management server in `localhost:15672` and create the vhost.

- The compose spins up a dagit server and a dagster worker. they use the same image but different entrypoints. Test the pipeline by going to `localhost:2001` select the `parallel_pipeline` and the preset `celery` in the playground