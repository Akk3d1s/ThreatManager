"""Import and configure all packages"""
from os.path import join, dirname, realpath
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
from config import Config

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads')
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_FILES_SIZE = 10000000 # 10mb

app = Flask(__name__, template_folder='views')
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)
url_safe_timed_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
MAX_CONFIRMATION_WAITING_TIME = 86400  # 24 hours
MAX_CONFIRMATION_RESEND_WAITING_TIME = 628800  # 8 hours

# noinspection Pylint
from app import models, controllers

## not imported elsewhere
# noinspection Pylint
from app.models.user_role import UserRole
# noinspection Pylint
from app.models.threat import Threat
# noinspection Pylint
from app.controllers.index import *
# noinspection Pylint
from app.controllers.login import *
# noinspection Pylint
from app.controllers.logout import *
# noinspection Pylint
from app.controllers.register import *
# noinspection Pylint
from app.controllers.report import *
# noinspection Pylint
from app.controllers.application_case import *
# noinspection Pylint
from app.controllers.application_role import *
# noinspection Pylint
from app.controllers.comment import *
# noinspection Pylint
from app.controllers.threat_list import *
# noinspection Pylint
from app.controllers.api_credential import *
# noinspection Pylint
from app.controllers.download import *
