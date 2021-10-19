# ThreatManager


## Installation

__Windows__
1) Navigate to ThreatManager: e.g. cd/ThreatManager
2) To create a virtual environment (recommended): Python -m venv venv
3) To activate the installed environment: venv\scripts\activate
4) While in the Venv environment: pip install -r requirements.txt
5) flask db init
6) python cli.py
7) init
8) flask run


__Linux and MacOS__
"python3 -m venv venv" (this will run the venv package and create a virtual environment called venv. We do this to not affect our global version of python)
to activate newly installed virtual environment type "source venv/bin/activate"
while in the venv environment:
- pip install flask
- pip install python-dotenv (to allow using an env file instead of setting the environment variables every time through the terminal)
- pip install flask-wtf (for handling forms)
- pip install flask-sqlalchemy (ORM for databases such as sql-lite, mysql etc)
- pip install flask-migrate (handy tool for handling robust changes to our database in the future)
- pip install flask-login
- pip install email-validator
- pip install flask-mail
- pip install pyjwt
- pip install safety (check for security vulnerabilities in the dependencies
- pip install pylint
- pip install pyflakes
- pip install flake8
- pip install pyotp
- pip install pytest
- pip install pytest-cov (coverage reports through "pytest -v --cov=app --cov-report=html"))
- flask db init (if migrations repo has not been created yet. usually only once, in the beginning of the project)


## Installation API (inside api directory)
__Linux and MacOS__
- pip install flask
- pip install flask-sqlalchemy (ORM for databases such as sql-lite, mysql etc)
- pip install flask_restful
- pip install python-dotenv
- pip install safety
- pip install pyjwt
# @todo - check linting and testing



## Running
### Serve the app
- flask run (should run at http://127.0.0.1:5000)

### Serve the API
- flask run inside the api directory (should run at http://127.0.0.1:5001)

### Updating DB schema
- flask db migrate (to generate migration scripts. these scripts are used to update the db schema according to the application code)
- flask db upgrade (to apply the changes in the migration script to the db schema)
- flask db downgrade (this will undo the last migration)

### Fresh rebuild
Use the CLI: "python cli.py" and then "init"


API NOTES
- For the sake of being distributed, the API was put into its own directory, without referencing code from the monolith app as the idea would be to deploy these seperately.
- The only resource the monolith and the API share, is the database.

OTHER NOTES
- We have knowlingly added the .flaskenv files to our repository, for the sake of easily having the same configuration among us. In a real world scenario, we do not recommend doing this.
