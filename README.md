# ThreatManager


## Installation
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
- pip install pyotp (https://www.section.io/engineering-education/implementing-totp-2fa-using-flask/)
- pip install pytest
- pip install pytest-cov (coverage reports through "pytest -v --cov=app --cov-report=html"))
- flask db init (if migrations repo has not been created yet. usually only once, in the beginning of the project)

## Running
### Serve the app
- flask run

### Updating DB schema
- flask db migrate (to generate migration scripts. these scripts are used to update the db schema according to the application code)
- flask db upgrade (to apply the changes in the migration script to the db schema)
- flask db downgrade (this will undo the last migration)

### Fresh rebuild
Use the CLI: "python cli.py" and then "init"
