from dagster_celery import celery_executor
from pathlib import Path
from dagster import ModeDefinition, default_executors, pipeline, solid, repository, PresetDefinition

celery_mode_defs = [ModeDefinition(name='default', executor_defs=default_executors + [celery_executor])]

celery_yaml_path = Path(__file__).parent / 'celery_execution.yaml'
presets = [PresetDefinition.from_files(name='celery', environment_files=[str(celery_yaml_path)], mode='default')]


@solid
def not_much(_):
    print('hello')
    return None


@pipeline(mode_defs=celery_mode_defs, preset_defs=presets)
def parallel_pipeline():
    for i in range(50):
        not_much.alias('not_much_' + str(i))()


@repository
def parallel_repo():
    return [parallel_pipeline]