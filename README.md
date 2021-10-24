# ThreatManager
Please run on Python 3.10.0 or higher

## Installation and running of the Monlith
__Linux, MacOS and most IDEs__
1_ Navigate to the root (e.g. cd /ThreatManager )
2) To run a virtual environment: "python3 -m venv venv"
3) Activate the newly installed virtual environment: source venv/bin/activate
4) While in the Venv environment: pip install -r requirements.txt
5) python cli.py
6) init
7) flask run (should run at http://127.0.0.1:5000)

__Windows Command Prompt_
1) Navigate to the root: e.g. cd ThreatManager
2) To create a virtual environment (recommended): python -m venv venv
3) To activate the installed environment: venv\scripts\activate
4) While in the Venv environment: pip install -r requirements.txt
5) python cli.py
6) init
7) flask run (should run at http://127.0.0.1:5000)

## Test roles for the marker
The Google Authenticator key for all of the below roles: 4HMSIHRWLTJM25VFB37FAGYSSZG2LER6

Citizen (can log threats):
Email: justin@gmail.com
Password: justin

Editor (can reply to citizen to ask for more information and forward cases to the approver):
Email: hendrik@police.com
Password: hendrik

Approver (can approve or reject cases)
Email: jonny@police.com
Password: jonny

Admin (can change user roles upon request):
Email: admin@police.com
Password: admin

Developer (can access the API):
Email: developer@police.com
Password: developer


## Installation and running of the API  (inside api directory)
1) Navigate to the directory: cd /ThreatManager/api (cd ThreatManager/api on Windows Command Prompt)
2) python3 -m venv venv
3) source venv/bin/activate
4) pip install -r requirements.txt
5) flask run inside the api directory (should run at http://127.0.0.1:5001)
6) Paste in http://127.0.0.1:5001/login to login
7) For login details please see the Developer email (username) and password above.
8) http://127.0.0.1:5001/[*]?token=[put API token in here]
	* = any of the above can go in the space above
	threats
	threats/[enter the threat id here]/files
	threats/[enter the threat id here]/files/<file_id>/download
	threats/[enter the threat id here]/comments


## Testing Monolith
- go into /tests directory
- run pytest

## Testing API
- go into /api directory
- run pytest


### Fresh rebuild
Use the CLI: "python cli.py" and then "init"


API NOTES
- For the sake of being distributed, the API was put into its own directory, without referencing code from the monolith app as the idea would be to deploy these seperately.
- The only resource the monolith and the API share, is the database.

OTHER NOTES
- We have knowlingly added the .flaskenv files to our repository, for the sake of easily having the same configuration among us. In a real world scenario, we do not recommend doing this.
