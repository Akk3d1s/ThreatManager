from flask import redirect, url_for, request
from flask_migrate import current
from app import app, db
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
