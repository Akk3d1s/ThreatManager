from flask import send_file, render_template, flash, redirect, url_for, request
from app import ALLOWED_EXTENSIONS, app, db
from app.forms import ThreatReportForm
from flask_login import current_user
from app.models.threat import Threat
from app.models.file import ThreatFile
from werkzeug.utils import secure_filename, send_from_directory
import os
from os.path import join, dirname, realpath, basename


@app.route('/download_threat/<int:threat_id>', methods=['GET', 'POST'])
def downloadThreatFile(threat_id=None):
    files = ThreatFile.query.filter(ThreatFile.threat_id==threat_id).all()
    filePath = join(dirname(realpath(__file__)))+'/../static/uploads/'
    if len(files)==1:
        return send_file(filePath+files[0].file, attachment_filename=files[0].file, as_attachment=True)
    else:
        zipFileName = 'threat'+str(threat_id)+'.zip'
        return send_file(filePath+zipFileName, mimetype='application/zip', attachment_filename=zipFileName, as_attachment=True)
    # return app.send_static_file('dutchpolice.png')
    # return send_file('./static/dutchpolice.png', mimetype='image/png', attachment_filename='dutchpolice.png', as_attachment=True) 
    # return send_file('./static/dutchpolice.png', mimetype='image/png', attachment_filename='dutchpolice.png', as_attachment=True) 
    # 'dutchpolice.png',mimetype='image/jpg')

