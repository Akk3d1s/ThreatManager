from flask import redirect, url_for, render_template, request
from flask_migrate import current
from app import app, db
from app.models.user import User
from app.models.user_role import UserRole
from app.models.application_role import RoleApplication
from flask_login import current_user, login_required
from app.helpers.authenticator import Authenticator
from app.helpers.id_validator import IdValidator
from app.helpers.logger import Logger


@app.route('/role_application/<int:role_id>', methods=['GET', 'POST'])
@login_required
def roleApplication(role_id=None):
    try:
        if not Authenticator.role_access_check(request.path):
            return redirect(url_for('index'))
        if not IdValidator.validateRoleID(role_id):
            return redirect(url_for('index'))
        if(RoleApplication.query.filter(RoleApplication.user_id==current_user.id).count()>=1):
            RoleApplication.query.filter(RoleApplication.user_id==current_user.id).delete()
        roleApplication = RoleApplication(user_id=current_user.id, role_id=role_id)
        roleApplication.save()
        Logger.success(request.path)
        return redirect(url_for('index'))
    except Exception as error:
        Logger.fail(request.path, error)
        return redirect(url_for('index'))

@app.route('/role_application_list', methods=['GET', 'POST'])
@login_required
def roleApplicationList():
    try:
        if not Authenticator.role_access_check(request.path):
            return redirect(url_for('index'))
        roleApplications = db.session.query(User, UserRole, RoleApplication).filter(User.id==RoleApplication.user_id).filter(UserRole.id==RoleApplication.role_id).all()
        Logger.success(request.path)
        return render_template("admin.html", title="Home Page", roleApplications=roleApplications)
    except Exception as error:
        Logger.fail(request.path, error)
        return redirect(url_for('index'))

@app.route('/role_application_approve/<int:role_application_id>', methods=['GET', 'POST'])
@login_required
def approveRoleApplication(role_application_id=None):
    try:
        if not Authenticator.role_access_check(request.path):
            return redirect(url_for('index'))
        if not IdValidator.validateRoleApplicationID(role_application_id):
            return redirect(url_for('index'))
        roleApplication = RoleApplication.query.filter(RoleApplication.id==role_application_id).first()
        user = User.query.filter(User.id==roleApplication.user_id).first()
        user.role_id = roleApplication.role_id
        RoleApplication.query.filter(RoleApplication.id==role_application_id).delete()
        db.session.commit()
        Logger.success(request.path)
        return redirect(url_for('roleApplicationList'))
    except Exception as error:
        Logger.fail(request.path, error)
        return redirect(url_for('index'))

@app.route('/role_application_reject/<int:role_application_id>', methods=['GET', 'POST'])
@login_required
def rejectRoleApplication(role_application_id=None):
    try:
        if not Authenticator.role_access_check(request.path):
            return redirect(url_for('index'))
        if not IdValidator.validateRoleApplicationID(role_application_id):
            return redirect(url_for('index'))
        RoleApplication.query.filter(RoleApplication.id==role_application_id).delete()
        Logger.success(request.path)
        return redirect(url_for('roleApplicationList'))
    except Exception as error:
        Logger.fail(request.path, error)
        return redirect(url_for('index'))