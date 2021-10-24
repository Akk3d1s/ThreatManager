from flask import flash, redirect, url_for, request
from flask_login import login_required
from app import app, db
from app.models.threat import Threat
from app.helpers.logger import Logger
from app.helpers.authenticator import Authenticator
from app.helpers.id_validator import IdValidator


@app.route('/newcase_application/<int:threat_id>', methods=['GET', 'POST'])
@login_required
def newcase(threat_id=None):
    try:
        if not Authenticator.role_access_check(request.path):
            return redirect(url_for('index'))
        if not IdValidator.validateThreatIDnCategoryID(threat_id):
            return redirect(url_for('index'))
        threat = Threat.query.filter_by(id=threat_id).first()
        threat.status_id = 2
        db.session.commit()
        Logger.success(request.path)
        return redirect(url_for('threat'))
    except Exception as error:
        Logger.fail(request.path, error)
        return redirect(url_for('threat'))


@app.route('/newcase_approve/<int:threat_id>/<int:category_id>', methods=[
    'GET', 'POST'])
@login_required
def approve_newcase(threat_id, category_id):
    try:
        if not Authenticator.role_access_check(request.path):
            return redirect(url_for('index'))
        if not IdValidator.validateThreatIDnCategoryID(threat_id, category_id):
            return redirect(url_for('index'))
        threat = Threat.query.filter_by(id=threat_id).first()
        threat.status_id = 3
        threat.category_id = category_id
        db.session.commit()
        Logger.success(request.path)
        return redirect(url_for('threat'))
    except Exception as error:
        Logger.fail(request.path, error)
        return redirect(url_for('threat'))



@app.route('/newcase_reject/<int:threat_id>', methods=['GET', 'POST'])
@login_required
def reject_newcase(threat_id=None):
    try:
        if not Authenticator.role_access_check(request.path):
            return redirect(url_for('index'))
        if not IdValidator.validateThreatIDnCategoryID(threat_id):
            return redirect(url_for('index'))
        threat = Threat.query.filter_by(id=threat_id).first()
        threat.status_id = 6
        db.session.commit()
        Logger.success(request.path)
        return redirect(url_for('threat'))
    except Exception as error:
        Logger.fail(request.path, error)
        return redirect(url_for('threat'))



@app.route('/endcase_application/<int:threat_id>', methods=['GET', 'POST'])
@login_required
def endcase(threat_id=None):
    try:
        if not Authenticator.role_access_check(request.path):
            return redirect(url_for('index'))
        if not IdValidator.validateThreatIDnCategoryID(threat_id):
            return redirect(url_for('index'))
        threat = Threat.query.filter_by(id=threat_id).first()
        threat.status_id = 4
        db.session.commit()
        Logger.success(request.path)
        return redirect(url_for('threat'))
    except Exception as error:
        Logger.fail(request.path, error)
        return redirect(url_for('threat'))



@app.route('/endcase_approve/<int:threat_id>', methods=['GET', 'POST'])
@login_required
def approve_endcase(threat_id=None):
    try:
        if not Authenticator.role_access_check(request.path):
            return redirect(url_for('index'))
        if not IdValidator.validateThreatIDnCategoryID(threat_id):
            return redirect(url_for('index'))
        threat = Threat.query.filter_by(id=threat_id).first()
        threat.status_id = 5
        db.session.commit()
        Logger.success(request.path)
        return redirect(url_for('threat'))
    except Exception as error:
        Logger.fail(request.path, error)
        return redirect(url_for('threat'))



@app.route('/endcase_reject/<int:threat_id>', methods=['GET', 'POST'])
@login_required
def reject_endcase(threat_id=None):
    try:
        if not Authenticator.role_access_check(request.path):
            return redirect(url_for('index'))
        if not IdValidator.validateThreatIDnCategoryID(threat_id):
            return redirect(url_for('index'))
        threat = Threat.query.filter_by(id=threat_id).first()
        threat.status_id = 3
        db.session.commit()
        Logger.success(request.path)
        return redirect(url_for('threat'))
    except Exception as error:
        Logger.fail(request.path, error)
        return redirect(url_for('threat'))

