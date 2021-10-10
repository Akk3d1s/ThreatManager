from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__, template_folder='views')
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)

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
