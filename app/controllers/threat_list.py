"""Deals with the the logging/viewing of threats depending on user type"""
from sqlalchemy import or_, func
from flask import render_template
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
from app.models.file import ThreatFile, CommentFile


@app.route('/threat')
@login_required
def threat():
    """Handles returning the correct views for the different roles"""
    try:
        # citizen role
        if current_user.role_id == 1:
            form = ThreatCommentForm()
            user_roles = db.session.query(UserRole).all()
            threats = db.session\
                .query(Threat, ThreatStatus, ThreatCategory, User, UserRole,func.count(ThreatFile.id)
                       .filter(ThreatFile.threat_id == Threat.id)
                       .label("file_count"))\
                .join(ThreatStatus)\
                .join(ThreatCategory)\
                .join(User)\
                .join(UserRole)\
                .filter(User.id == current_user.id)\
                .group_by(Threat)\
                .all()
            # comments = db.session.query(Comment, User, UserRole.role,func.count(CommentFile.id).filter(CommentFile.comment_id == Comment.id).label("file_count")).join(Comment).join(UserRole).group_by(Comment).all()
            comments = db.session\
                .query(Comment, User, UserRole, func.count(CommentFile.id)
                       .filter(CommentFile.comment_id == Comment.id)
                       .label("file_count"))\
                .filter(Comment.user_id == User.id)\
                .filter(User.role_id == UserRole.id)\
                .group_by(Comment)\
                .all()
            case_count = db.session\
                .query(func.count(Threat.id)
                       .filter(or_(Threat.status_id == 1,Threat.status_id == 2))
                       .label("new_case"), func.count(Threat.id)
                       .filter(or_(Threat.status_id == 3, Threat.status_id == 4))
                       .label("resolving_case"), func.count(Threat.id).
                       filter(Threat.status_id == 5)
                       .label("resolved_case"), func.count(Threat.id)
                       .filter(Threat.status_id == 6)
                       .label("rejected_case"), func.count(Threat.id)
                       .filter(Threat.status_id == 7)
                       .label("cancelled_case"))\
                .first()
            return render_template("citizen.html",
                                   title='Home Page',
                                   threats=threats,
                                   comments=comments,
                                   userRoles=user_roles,
                                   caseCount=case_count,
                                   form=form)
        # police roles
        elif current_user.role_id == 4:
            form = ThreatCommentForm()
            user_roles = db.session.query(UserRole).all()
            threats = db.session\
                .query(Threat, ThreatStatus, ThreatCategory, User, UserRole,func.count(ThreatFile.id)
                       .filter(ThreatFile.threat_id == Threat.id)
                       .label("file_count"))\
                .join(ThreatStatus)\
                .join(ThreatCategory)\
                .join(User)\
                .join(UserRole)\
                .filter(or_(ThreatStatus.status == "APPROVINGNEWCASE", ThreatStatus.status == "APPROVINGENDCASE"))\
                .group_by(Threat)\
                .all()
            comments = db.session\
                .query(Comment, User, UserRole, func.count(CommentFile.id)
                       .filter(CommentFile.comment_id == Comment.id)
                       .label("file_count"))\
                .filter(Comment.user_id == User.id)\
                .filter(User.role_id == UserRole.id)\
                .group_by(Comment)\
                .all()
            case_count = db.session\
                .query(func.count(Threat.id)
                       .filter(or_(Threat.status_id == 1,Threat.status_id == 2))
                       .label("new_case"), func.count(Threat.id)
                       .filter(or_(Threat.status_id == 3, Threat.status_id == 4))
                       .label("resolving_case"), func.count(Threat.id)
                       .filter(Threat.status_id == 5)
                       .label("resolved_case"), func.count(Threat.id)
                       .filter(Threat.status_id == 6)
                       .label("rejected_case"), func.count(Threat.id)
                       .filter(Threat.status_id == 7)
                       .label("cancelled_case"))
            first()
            threat_categories = db.session.query(ThreatCategory).all()
            return render_template("approver.html",
                                   title="Home Page",
                                   userRoles=user_roles,
                                   threats=threats,
                                   comments=comments,
                                   caseCount=case_count,
                                   threatCategories=threat_categories,
                                   form=form)
        elif current_user.role_id == 6:
            role_applications = db.session\
                .query(User, UserRole, RoleApplication)\
                .filter(User.id == RoleApplication.user_id)\
                .filter(UserRole.id == RoleApplication.role_id)\
                .all()
            return render_template("admin.html",
                                   title="Home Page",
                                   roleApplications=role_applications)
        else:
            form = ThreatCommentForm()
            user_roles = db.session.query(UserRole).all()
            threats = db.session\
                .query(Threat, ThreatStatus, ThreatCategory, User, UserRole,func.count(ThreatFile.id)
                       .filter(ThreatFile.threat_id == Threat.id)
                       .label("file_count"))\
                .join(ThreatStatus)\
                .join(ThreatCategory)\
                .join(User)\
                .join(UserRole)\
                .group_by(Threat)\
                .all()
            comments = db.session\
                .query(Comment, User, UserRole, func.count(CommentFile.id)
                       .filter(CommentFile.comment_id == Comment.id)
                       .label("file_count"))\
                .filter(Comment.user_id == User.id)\
                .filter(User.role_id == UserRole.id)\
                .group_by(Comment)\
                .all()
            case_count = db.session\
                .query(func.count(Threat.id)
                       .filter(or_(Threat.status_id == 1,Threat.status_id == 2))
                       .label("new_case"), func.count(Threat.id)
                       .filter(or_(Threat.status_id == 3, Threat.status_id == 4))
                       .label("resolving_case"), func.count(Threat.id)
                       .filter(Threat.status_id == 5)
                       .label("resolved_case"), func.count(Threat.id)
                       .filter(Threat.status_id == 6)
                       .label("rejected_case"), func.count(Threat.id)
                       .filter(Threat.status_id == 7)
                       .label("cancelled_case"))\
                .first()
            if current_user.role_id == 2:
                return render_template("viewer.html",
                                       title='Home Page',
                                       userRoles=user_roles,
                                       threats=threats,
                                       comments=comments,
                                       caseCount=case_count,
                                       form=form)
            elif current_user.role_id == 3:
                return render_template("editor.html",
                                       title='Home Page',
                                       userRoles=user_roles,
                                       threats=threats,
                                       comments=comments,
                                       caseCount=case_count,
                                       form=form)
            elif current_user.role_id == 5:
                return render_template("developer.html",
                                       title="Home Page",
                                       userRoles=user_roles,
                                       threats=threats,
                                       comments=comments,
                                       threatCategories=threat_categories,
                                       form=form)
    except Exception as error:
        print(error)
