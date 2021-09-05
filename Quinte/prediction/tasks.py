from invoke import task

import app

@task
def start_single(c):
    app.single_work() 