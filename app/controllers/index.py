from flask import render_template
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_required
from app.models.user import User
from app.models.threat import Threat
from app.models.threat_status import ThreatStatus
from app.models.threat_category import ThreatCategory
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required
def index():
    # citizen role
    if current_user.role_id == 10:
        # threats = current_user.threats
        threats = db.session.query(User, Threat, ThreatStatus, ThreatCategory).filter(User.id==Threat.user_id).filter(Threat.status_id==ThreatStatus.id).filter(Threat.category_id==ThreatCategory.id).filter(User.id==current_user.id).all()
        return render_template("citizen.html", title='Home Page', threats=threats)
    # police roles
    elif current_user.role_id == 2:
        threats = db.session.query(User, Threat, ThreatStatus, ThreatCategory).filter(User.id==Threat.user_id).filter(Threat.status_id==ThreatStatus.id).filter(Threat.category_id==ThreatCategory.id).all()
        return render_template("view.html", title="Home Page", threats=threats)
    elif current_user.role_id == 11:
        threats = db.session.query(User, Threat, ThreatStatus, ThreatCategory).filter(User.id==Threat.user_id).filter(Threat.status_id==ThreatStatus.id).filter(Threat.category_id==ThreatCategory.id).all()
        return render_template("editor.html", title='Home Page', threats=threats)
    else:
        threats = db.session.query(User, Threat, ThreatStatus, ThreatCategory).filter(User.id==Threat.user_id).filter(Threat.status_id==ThreatStatus.id).filter(Threat.category_id==ThreatCategory.id).filter(Threat.status_id==2).all()
        return render_template("approver.html", title="Home Page", threats=threats)
        