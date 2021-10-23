from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_required
from app import app, db
from app.forms import ThreatCommentForm
from app.models.user import User
from app.models.user_role import UserRole
from app.models.threat import Threat
from app.models.threat_status import ThreatStatus
from app.models.threat_category import ThreatCategory
from app.models.comment import Comment
from app.models.application_role import RoleApplication
from app.helpers.authenticator import Authenticator
from sqlalchemy import or_

@app.route('/api_credential')
@login_required
def api_credential():
    if not Authenticator.route_access_check(request.path):
        return redirect(url_for('index'))
    # citizen role
    if current_user.role_id == 1:
        # threats = current_user.threats
        # threats = db.session.query(User, Threat, ThreatStatus,
        # ThreatCategory).filter(User.id==Threat.user_id).filter(
        # Threat.status_id==ThreatStatus.id).filter(
        # Threat.category_id==ThreatCategory.id).filter(
        # User.id==current_user.id).all()
        form = ThreatCommentForm()
        user_roles = db.session.query(UserRole).all()
        threats = db.session.query(
            User, UserRole, Threat, ThreatStatus, ThreatCategory).filter(
            User.role_id == UserRole.id).filter(
            User.id == Threat.user_id).filter(
            Threat.status_id == ThreatStatus.id).filter(
            Threat.category_id == ThreatCategory.id).filter(
            User.id == current_user.id).all()
        comments = db.session.query(User, UserRole, Comment).filter(
            User.role_id == UserRole.id).filter(
            User.id == Comment.user_id).all()
        return render_template(
            "citizen.html", title='Home Page', threats=threats,
            comments=comments, userRoles=user_roles, form=form)
    # police roles
    elif current_user.role_id == 2:
        threats = db.session.query(
            User, Threat, ThreatStatus, ThreatCategory).filter(
            User.id == Threat.user_id).filter(
            Threat.status_id == ThreatStatus.id).filter(
            Threat.category_id == ThreatCategory.id).all()
        return render_template(
            "citizen.html", title="Home Page", threats=threats)
    elif current_user.role_id == 3:
        form = ThreatCommentForm()
        user_roles = db.session.query(UserRole).all()
        threats = db.session.query(
            User, UserRole, Threat, ThreatStatus, ThreatCategory).filter(
            User.role_id == UserRole.id).filter(
            User.id == Threat.user_id).filter(
            Threat.status_id == ThreatStatus.id).filter(
            Threat.category_id == ThreatCategory.id).all()
        comments = db.session.query(User, UserRole, Comment).filter(
            User.role_id == UserRole.id).filter(
            User.id == Comment.user_id).all()
        return render_template(
            "editor.html", title='Home Page', userRoles=user_roles,
            threats=threats, comments=comments, form=form)
    elif current_user.role_id == 4:
        form = ThreatCommentForm()
        user_roles = db.session.query(UserRole).all()
        threats = db.session.query(
            User, UserRole, Threat, ThreatStatus, ThreatCategory).filter(
            User.role_id == UserRole.id).filter(
            User.id == Threat.user_id).filter(
            Threat.status_id == ThreatStatus.id).filter(
            Threat.category_id == ThreatCategory.id).filter(
            or_(Threat.status_id == 2, Threat.status_id == 4)).all()
        comments = db.session.query(User, UserRole, Comment).filter(
            User.role_id == UserRole.id).filter(
            User.id == Comment.user_id).all()
        threat_categories = db.session.query(ThreatCategory).all()
        return render_template(
            "approver.html", title="Home Page",
            userRoles=user_roles, threats=threats,
            comments=comments, threatCategories=threat_categories, form=form)
    else:
        role_applications = db.session.query(
            User, UserRole, RoleApplication).filter(
            User.id == RoleApplication.user_id).filter(
            UserRole.id == RoleApplication.role_id).all()
        return render_template(
            "admin.html", title="Home Page", roleApplications=role_applications)
