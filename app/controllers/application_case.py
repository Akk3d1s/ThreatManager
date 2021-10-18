from flask import redirect, url_for, request
from app import app, db
from app.models.threat import Threat
from app.helpers.authenticator import Authenticator


@app.route('/newcase_application/<int:threat_id>', methods=['GET', 'POST'])
def newcase(threat_id=None):
    if not Authenticator.route_access_check(request.path):
        return redirect(url_for('index'))
    threat = Threat.query.filter_by(id=threat_id).first()
    threat.status_id = 2
    db.session.commit()
    return redirect(url_for('threat'))

@app.route('/newcase_approve/<int:threat_id>/<int:category_id>', methods=['GET', 'POST'])
def approveNewcase(threat_id, category_id):
    if not Authenticator.route_access_check(request.path):
        return redirect(url_for('index'))
    threat = Threat.query.filter_by(id=threat_id).first()
    threat.status_id = 3
    threat.category_id = category_id
    db.session.commit()
    return redirect(url_for('threat'))

@app.route('/newcase_reject/<int:threat_id>', methods=['GET', 'POST'])
def rejectNewcase(threat_id=None):
    if not Authenticator.route_access_check(request.path):
        return redirect(url_for('index'))
    threat = Threat.query.filter_by(id=threat_id).first()
    threat.status_id = 6
    db.session.commit()
    return redirect(url_for('threat'))

@app.route('/endcase_application/<int:threat_id>', methods=['GET', 'POST'])
def endcase(threat_id=None):
    if not Authenticator.route_access_check(request.path):
        return redirect(url_for('index'))
    threat = Threat.query.filter_by(id=threat_id).first()
    threat.status_id = 4
    db.session.commit()
    return redirect(url_for('threat'))

@app.route('/endcase_approve/<int:threat_id>', methods=['GET', 'POST'])
def approveEndcase(threat_id=None):
    if not Authenticator.route_access_check(request.path):
        return redirect(url_for('index'))
    threat = Threat.query.filter_by(id=threat_id).first()
    threat.status_id = 5
    db.session.commit()
    return redirect(url_for('threat'))

@app.route('/endcase_reject/<int:threat_id>', methods=['GET', 'POST'])
def rejectEndcase(threat_id=None):
    if not Authenticator.route_access_check(request.path):
        return redirect(url_for('index'))
    threat = Threat.query.filter_by(id=threat_id).first()
    threat.status_id = 3
    db.session.commit()
    return redirect(url_for('threat'))
