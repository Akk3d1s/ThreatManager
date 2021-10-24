"""
This module contains the the functions handling routes relating to:
The Editor starting cases and ending cases.
the Approver accepting or rejecting cases, and accepting
and rejecting the ending of cases.
This module modifies the status_id column in
the Threat table based upon the above.
All .hmtl files referred to are in the views folder
(route: ThreatManager/app/views).
"""
from flask import redirect, url_for, request
from flask_login import login_required
from app import app, db
from app.models.threat import Threat
from app.helpers.logger import Logger
from app.helpers.authenticator import Authenticator
from app.helpers.id_validator import IdValidator


@app.route('/newcase_application/<int:threat_id>', methods=['GET', 'POST'])
@login_required
def newcase(threat_id=None):
    """
    Within the editor.html file there is a button labelled "new case"
    adjacent to cases that have been logged by a citizen but not
    yet had a "new case" started. Clicking on this button directs to
    the /newcase_application route. This function
    then changes the Status_id to 2 in the Threat table.
    The Editor is then returned to the /threat route.
    """
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
    """
    Within the approver.html file there is a button labelled "approve" adjacent
    to cases which have been started by the Editor.
    Clicking on this directs to the /newcase_approve route.
    This function changes the Status_id to 3 in the Threat table and returns
    the Approver to the /threat route.
    """
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
    """
    Within the approver.html file there is a button labelled "reject" adjacent
    to cases which have been started by the Editor.
    Clicking on this directs to the /newcase_reject route.
    This function changes the Status_id to 6 in the Threat table and returns
    the Approver to the /threat route.
    """
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
    """
    Within the editor.html file there is a button labelled "End Case" adjacent
    to cases which have been accepted by the Approver.
    Clicking on this directs to the /endcase_application route.
    This function changes the Status_id to 4 in the Threat table and returns
    the Editor to the /threat route.
    """
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
    """
    Within the approver.html file there is a button labelled "Accept" adjacent
    to cases which have been ended by the Editor.
    Clicking on this directs to the /endcase_application route.
    This function changes the Status_id to 5 in the Threat table and returns
    the Approver to the /threat route.
    """
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
    """
    Within the approver.html file there is a button labelled "Reject" adjacent
    to cases which have been ended by the Editor.
    Clicking on this directs to the /endcase_application route.
    This function changes the Status_id to 3 in the Threat table and returns
    the Approver to the /threat route.
    """
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
