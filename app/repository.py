from dagster_celery import celery_executor
from pathlib import Path
from dagster import ModeDefinition, default_executors, pipeline, solid, repository, PresetDefinition, default_system_storage_defs
from dagster_aws.s3 import s3_system_storage, s3_resource

import numpy as np

celery_mode_defs = [
    ModeDefinition(
        name='default',
        resource_defs={'s3': s3_resource},
        executor_defs=default_executors + [celery_executor],
        system_storage_defs=default_system_storage_defs + [s3_system_storage]
    )]

celery_yaml_path = Path(__file__).parent / 'celery_execution.yaml'
presets = [PresetDefinition.from_files(name='celery', environment_files=[str(celery_yaml_path)], mode='default')]


@solid
def generate_number(_):
    print('hello')
    num = np.random.randint(low=1, high=100)
    return num


@solid
def square_number(_, number):
    square = np.power(number, 2)
    return square


@pipeline(mode_defs=celery_mode_defs, preset_defs=presets)
def parallel_pipeline():
    for i in range(20):
        number_pipe = generate_number.alias('generate_number_' + str(i))()
        square_number.alias('square_number_'+str(i))(number_pipe)


@repository
def parallel_repo():
    return [parallel_pipeline]
