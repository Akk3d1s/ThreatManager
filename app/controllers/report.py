from flask import render_template, flash, redirect, url_for, request
from app import ALLOWED_EXTENSIONS, ALLOWED_FILES_SIZE, app, db
from app.forms import ThreatReportForm
from flask_login import current_user, login_required
from app.models.threat import Threat
from app.models.file import ThreatFile
from werkzeug.utils import secure_filename
import os
from os.path import join, dirname, realpath, basename
from zipfile import ZipFile
from app.helpers.authenticator import Authenticator
from app.helpers.logger import Logger

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def requestFileValidation():
    fileList = request.files.getlist('file')
    print(fileList)
    if len(fileList)>20:
        flash("Over than 20 files")
        return False
    fileSize = 0
    for file in fileList:
        file.seek(0, os.SEEK_END)
        fileSize += file.tell()
        print("fileSize: ")
        print(fileSize)
        if fileSize > ALLOWED_FILES_SIZE:
            flash("Size of files over the limit of 10 MB")
            return False
        if allowed_file(file.filename) == False:
            flash("Invalid file type")
            return False
    return True

def requestFileSaveZip(threat_id):
    fileCount = len(request.files.getlist('file'))
    if fileCount == 1: # single file no need zip
        file = request.files['file']
        filename = "threat"+str(threat_id)+"_"+secure_filename(file.filename)
        file.seek(0)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file = ThreatFile(file=filename, threat_id=threat_id)
        db.session.add(file)
        db.session.commit()
        return redirect(url_for('threat'))
    elif fileCount > 1:
        filePath = join(dirname(realpath(__file__)))+'/../static/uploads'
        zipObj = ZipFile(filePath + '/threat'+str(threat_id)+'.zip', 'w')
        for file in request.files.getlist('file'):
            filename = "threat"+str(threat_id)+"_"+secure_filename(file.filename)
            file.seek(0)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            zipObj.write(filePath+'/'+filename, basename(filePath+'/'+filename))
            file = ThreatFile(file=filename, threat_id=threat_id)
            db.session.add(file)
            db.session.commit()
        zipObj.close()
        return redirect(url_for('threat'))

@app.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    try:
        if not Authenticator.role_access_check(request.path):
            return redirect(url_for('index'))
        form = ThreatReportForm()
        if form.validate_on_submit() and 'file' in request.files:
            if not requestFileValidation():
                return redirect(url_for('report'))
            threat = Threat(title=form.title.data, description=form.description.data, reproduce_steps=form.reproduce_steps.data, user_id=current_user.id, status_id=1, category_id=1)
            db.session.add(threat)
            db.session.commit()
            requestFileSaveZip(threat.id)
            Logger.success(request.path)
            return redirect(url_for('threat'))
        return render_template('report.html', title='Report', form=form)
    except Exception as error:
        Logger.fail(request.path, error)
        return redirect(url_for('threat'))
