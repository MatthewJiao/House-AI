Setup (First time on machine)

(windows)

set up virtual environment
- python -m venv --system-site-packages .\venv
- .\venv\Scripts\activate
- pip install --upgrade pip
- deactivate (to exit later)

then run

- pip install -r requirements.txt
to install the packages and requirements


Make sure the vscode python version is the one with '(venv)' ie. Python 3.8.6 64-bit ('venv': venv)

Then in terminal, cd into prediction, then run invoke -l for a list of runnable tasks from the terminal.