from invoke import task

import app
import metrics

@task
def start_single(c):
    #starts a single worker for a single patient
    app.single_work() 

@task
def test_rules(c):
    #comprehensively tests the rules portion
    c.run("python -m pytest -rP tests_rules.py")

@task
def run_metrics(c):
    metrics.run_on_dataset()