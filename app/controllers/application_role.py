from flask import redirect, url_for, render_template, request
from flask_migrate import current
from app import app, db
from app.models.user import User
from app.models.user_role import UserRole
from app.models.application_role import RoleApplication
from flask_login import current_user, login_required
from app.helpers.authenticator import Authenticator
from app.helpers.logger import Logger

@app.route('/role_application/<int:role_id>', methods=['GET', 'POST'])
@login_required
def role_application(role_id=None):
    try:
        if not Authenticator.route_access_check(request.path):
            return redirect(url_for('index'))
        if(RoleApplication.query.filter(RoleApplication.user_id==current_user.id).count()>=1):
            RoleApplication.query.filter(RoleApplication.user_id==current_user.id).delete()
        role_application = RoleApplication(user_id=current_user.id, role_id=role_id)
        db.session.add(role_application)
        db.session.commit()
        Logger.success(request.path)
        return redirect(url_for('index'))
    except Exception as error:
        Logger.fail(request.path, error)
        return redirect(url_for('index'))

@app.route('/role_application_list', methods=['GET', 'POST'])
@login_required
def role_application_list():
    try:
        if not Authenticator.route_access_check(request.path):
            return redirect(url_for('index'))
        role_applications = db.session.query(User, UserRole, RoleApplication).filter(User.id==RoleApplication.user_id).filter(UserRole.id==RoleApplication.role_id).all()
        Logger.success(request.path)
        return render_template("admin.html", title="Home Page", roleApplications=role_applications)
    except Exception as error:
        Logger.fail(request.path, error)
        return redirect(url_for('index'))

@app.route('/role_application_approve/<int:role_application_id>', methods=['GET', 'POST'])
@login_required
def approve_role_application(role_application_id=None):
    try:
        if not Authenticator.route_access_check(request.path):
            return redirect(url_for('index'))
        role_application = RoleApplication.query.filter(RoleApplication.id==role_application_id).first()
        user = User.query.filter(User.id==role_application.user_id).first()
        user.role_id = role_application.role_id
        RoleApplication.query.filter(RoleApplication.id==role_application_id).delete()
        db.session.commit()
        Logger.success(request.path)
        return redirect(url_for('role_application_list'))
    except Exception as error:
        Logger.fail(request.path, error)
        return redirect(url_for('index'))

@app.route('/role_application_reject/<int:role_application_id>', methods=['GET', 'POST'])
@login_required
def reject_role_application(role_application_id=None):
    try:
        if not Authenticator.route_access_check(request.path):
            return redirect(url_for('index'))
        RoleApplication.query.filter(RoleApplication.id==role_application_id).delete()
        Logger.success(request.path)
        return redirect(url_for('role_application_list'))
    except Exception as error:
        Logger.fail(request.path, error)
        return redirect(url_for('index'))