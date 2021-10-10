from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from os.path import join, dirname, realpath
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__, template_folder='views')
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)
url_safe_timed_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
max_confirmation_waiting_time = 86400  # 24 hours
max_confirmation_resend_waiting_time = 628800  # 8 hours

from app import models, controllers

## not imported elsewhere
from app.models.user_role import UserRole
from app.models.threat import Threat
from app.controllers.index import *
from app.controllers.login import *
from app.controllers.logout import *
from app.controllers.register import *
from app.controllers.report import *
from app.controllers.application_case import *
from app.controllers.application_role import *
from app.controllers.comment import *
