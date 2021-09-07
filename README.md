# ThreatManager


## installation
"python3 -m venv venv" (this will run the venv package and create a virtual environment called venv. We do this to not affect our global version of python)
to activate newly installed virtual environment type "source venv/bin/activate"
while in the venv environment, 
    INSTALLING - execute the following commands(to keep it from being installed globally):
    -------------------------------------------------------------------------
    pip install flask
    pip install python-dotenv (to allow using an env file instead of setting the environment variables every time through the terminal)
    pip install flask-wtf (for handling forms)
    RUNNING - creating global variables so that flask knows how to execute the application
    ---------------------------------------------------------------------------------------
    export FLASK_APP=threatmanager.py (not needed if python-dotenv was installed and .flaskenv created with correct variables)
    flask run
