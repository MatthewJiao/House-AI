from invoke import task

import app

@task
def start(c):
    app.single_work() 