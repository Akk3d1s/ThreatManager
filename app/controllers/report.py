from flask import render_template, flash, redirect, url_for, request
from app import ALLOWED_EXTENSIONS, app, db
from app.forms import ThreatReportForm
from flask_login import current_user
from app.models.threat import Threat
from app.models.file import File
from werkzeug.utils import secure_filename
import os

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/report', methods=['GET', 'POST'])
def report():
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    form = ThreatReportForm()
    if form.validate_on_submit() and 'file' in request.files:
        # loop for uploaded files' extensions, if not valid return
        for file in request.files.getlist('file'):
            filename = secure_filename(file.filename)
            if allowed_file(filename) == False:
                print("false extension")
                flash("invalid file type")
                return render_template('report.html', title='Report', form=form)
        threat = Threat(title=form.title.data, description=form.description.data, reproduce_steps=form.reproduce_steps.data, user_id=current_user.id, status_id=1, category_id=1)
        db.session.add(threat)
        db.session.commit()
        # loop for saving the
        for file in request.files.getlist('file'):
            filename = "t"+str(threat.id)+"_"+secure_filename(file.filename)
            # if file and allowed_file(filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file = File(file=filename, threat_id=threat.id)
            db.session.add(file)
            db.session.commit()
            print('upload completed')
        return redirect(url_for('index'))
    return render_template('report.html', title='Report', form=form)