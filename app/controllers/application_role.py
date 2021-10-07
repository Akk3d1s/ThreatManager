from flask import redirect, url_for, request
from flask_migrate import current
from app import app, db
from app.models.user import User
from app.models.application_role import RoleApplication
from flask_login import current_user

@app.route('/role_application/<int:role_id>', methods=['GET', 'POST'])
def roleApplication(role_id=None):
    if(RoleApplication.query.filter(RoleApplication.user_id==current_user.id).count()>=1):
        RoleApplication.query.filter(RoleApplication.user_id==current_user.id).delete()
    roleApplication = RoleApplication(user_id=current_user.id, role_id=role_id)
    db.session.add(roleApplication)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/role_application_approve/<int:role_application_id>', methods=['GET', 'POST'])
def approveRoleApplication(role_application_id=None):
    roleApplication = RoleApplication.query.filter(RoleApplication.id==role_application_id).first()
    user = User.query.filter(User.id==roleApplication.user_id).first()
    user.role_id = roleApplication.role_id
    RoleApplication.query.filter(RoleApplication.id==role_application_id).delete()
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/role_application_reject/<int:role_application_id>', methods=['GET', 'POST'])
def rejectRoleApplication(role_application_id=None):
    RoleApplication.query.filter(RoleApplication.id==role_application_id).delete()
    return redirect(url_for('index'))