from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.models.threat import Threat
from flask_login import current_user


@app.route('/startcase/<int:threat_id>', methods=['GET', 'POST'])
def start(threat_id=None):
    threat = Threat.query.filter_by(id=threat_id).first()
    threat.status_id = 2
    db.session.commit()
    return redirect(url_for('index'))