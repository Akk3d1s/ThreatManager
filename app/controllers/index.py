"""Main entry of the application"""
from flask import render_template
from app import app, db
from flask_login import login_required
from app.models.user_role import UserRole
from app.models.application_role import RoleApplication

@app.route('/')
@app.route('/index')
@login_required
def index():
    """Home page"""
    role_application = db.session.query(RoleApplication).first()
    user_roles = db.session.query(UserRole).all()
    return render_template("dashboard.html",
                           title='Home Page',
                           userRoles=user_roles,
                           roleApplication=role_application)

