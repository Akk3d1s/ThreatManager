from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import ThreatReportForm
from flask_login import current_user
from app.models.threat import Threat


@app.route('/report', methods=['GET', 'POST'])
def report():
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    form = ThreatReportForm()
    if form.validate_on_submit():
        threat = Threat(title=form.title.data, description=form.description.data, reproduce_steps=form.reproduce_steps.data, user_id=current_user.id, status_id=1, category_id=1)
        db.session.add(threat)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('report.html', title='Report', form=form)