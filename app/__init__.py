from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app import models, controllers

## not imported elsewhere
from app.models.user_role import UserRole
from app.models.threat import Threat
from app.controllers.index import *
from app.controllers.login import *
from app.controllers.logout import *
from app.controllers.register import *
from app.controllers.report import *
from app.controllers.startcase import *