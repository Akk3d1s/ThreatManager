from flask import render_template
from app import app, db
from app.forms import ThreatCommentForm
from flask_login import current_user, login_required
from app.models.user import User
from app.models.user_role import UserRole
from app.models.threat import Threat
from app.models.threat_status import ThreatStatus
from app.models.threat_category import ThreatCategory
from app.models.comment import Comment
from app.models.application_role import RoleApplication
from app.models.file import ThreatFile
from werkzeug.urls import url_parse
from sqlalchemy import and_, or_, not_, func

@app.route('/threat')
@login_required
def threat():
    # citizen role
    if current_user.role_id == 1:
        form = ThreatCommentForm()
        userRoles = db.session.query(UserRole).all()
        threats = db.session.query(Threat, ThreatStatus, ThreatCategory, User, UserRole, func.count(ThreatFile.id).filter(ThreatFile.threat_id==Threat.id).label("file_count")).join(ThreatStatus).join(ThreatCategory).join(User).join(UserRole).group_by(Threat).all()
        comments = db.session.query(User, Comment, UserRole).join(Comment).join(UserRole).all()
        return render_template("citizen.html", title='Home Page', threats=threats, comments=comments, userRoles=userRoles, form=form)
    # police roles
    elif current_user.role_id == 2:
        threats = db.session.query(User, Threat, ThreatStatus, ThreatCategory).filter(User.id==Threat.user_id).filter(Threat.status_id==ThreatStatus.id).filter(Threat.category_id==ThreatCategory.id).all()
        return render_template("citizen.html", title="Home Page", threats=threats)
    elif current_user.role_id == 3:
        form = ThreatCommentForm()
        userRoles = db.session.query(UserRole).all()
        threats = db.session.query(Threat, ThreatStatus, ThreatCategory, User, UserRole).join(ThreatStatus).join(ThreatCategory).join(User).join(UserRole).all()
        comments = db.session.query(User, Comment, UserRole).join(Comment).join(UserRole).all()
        return render_template("editor.html", title='Home Page', userRoles=userRoles, threats=threats, comments=comments, form=form)
    elif current_user.role_id == 4:
        form = ThreatCommentForm()
        userRoles = db.session.query(UserRole).all()
        threats = db.session.query(Threat, ThreatStatus, ThreatCategory, User, UserRole).join(ThreatStatus).join(ThreatCategory).join(User).join(UserRole).all()
        comments = db.session.query(User, Comment, UserRole).join(Comment).join(UserRole).all()
        threatCategories = db.session.query(ThreatCategory).all()
        return render_template("approver.html", title="Home Page", userRoles=userRoles, threats=threats, comments=comments, threatCategories=threatCategories, form=form)
    else:
        roleApplications = db.session.query(User, UserRole, RoleApplication).filter(User.id==RoleApplication.user_id).filter(UserRole.id==RoleApplication.role_id).all()
        return render_template("admin.html", title="Home Page", roleApplications=roleApplications)
        