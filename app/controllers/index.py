from flask import render_template
from app import app, db
from app.forms import ThreatCommentForm
from flask_login import current_user, login_required
from app.models.user import User
from app.models.user_role import UserRole
from app.models.application_role import RoleApplication
from werkzeug.urls import url_parse
from sqlalchemy import and_, or_, not_

@app.route('/')
@app.route('/index')
@login_required
def index():
    try:
        role_application = db.session.query(RoleApplication).first()
        user_roles = db.session.query(UserRole).all()
        return render_template("dashboard.html", title='Home Page', userRoles=user_roles, roleApplication=role_application)
    except Exception as error:
        print(error)
        return render_template("dashboard.html", title='Home Page', userRoles=user_roles, roleApplication=role_application)

        