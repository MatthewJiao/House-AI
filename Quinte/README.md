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

See tasks.py for the task list and documentation.

pt_identifier, 0, 120, 80, 65, 37, 20, 100, 57, Male, 0, 0.5-2.2, 0, 4-11, 
pt_identifier, 30, 100, 77, 75, 37, 22, 98, 57, Male, 0, 0.5-2.2, 0, 4-11, 
pt_identifier, 60, 90, 74, 85, 38, 23, 99, 57, Male, 0, 0.5-2.2, 0, 4-11, 
pt_identifier, 90, 87, 72, 95, 39, 24, 99, 57, Male, 3.5, 0.5-2.2, 5, 4-11

pt_identifier, 0, 100, 80, 75, 37, 20, 100, 47, Female, 0, 0.5-2.2, 0, 4-11, 
pt_identifier, 30, 110, 77, 77, 37, 18, 98, 47, Female, 0, 0.5-2.2, 0, 4-11, 
pt_identifier, 60, 112, 78, 65, 37, 16, 99, 47, Female, 0, 0.5-2.2, 0, 4-11, 
pt_identifier, 90, 115, 76, 66, 37, 17, 99, 47, Female, 1.3, 0.5-2.2, 5.2, 4-11