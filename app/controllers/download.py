from flask import send_file, make_response, request, redirect, url_for
from flask_migrate import current
from app import ALLOWED_EXTENSIONS, app, db
from flask_login import current_user, login_required
from app.models.user import User
from app.models.user_role import UserRole
from app.models.threat import Threat
from app.models.threat_status import ThreatStatus
from app.models.threat_category import ThreatCategory
from app.models.file import ThreatFile, CommentFile
from sqlalchemy import func
from werkzeug.utils import secure_filename, send_from_directory
from os.path import join, dirname, realpath, basename
from io import StringIO
import csv
import datetime
from app.helpers.authenticator import Authenticator
from app.helpers.logger import Logger


@app.route('/download_file_threat/<int:threat_id>', methods=['GET', 'POST'])
@login_required
def downloadThreatFile(threat_id=None):
    try:
        if not Authenticator.route_access_check(request.path):
            return redirect(url_for('index'))
        files = ThreatFile.query.filter(ThreatFile.threat_id==threat_id).all()
        filePath = join(dirname(realpath(__file__)))+'/../static/uploads/'
        if len(files)==1:
            Logger.success(request.path)
            return send_file(filePath+files[0].file, attachment_filename=files[0].file, as_attachment=True)
        else:
            zipFileName = 'threat'+str(threat_id)+'.zip'
            Logger.success(request.path)
            return send_file(filePath+zipFileName, mimetype='application/zip', attachment_filename=zipFileName, as_attachment=True)
    except Exception as error:
        Logger.fail(request.path, error)
        return redirect(url_for('index'))

@app.route('/download_file_comment/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def downloadCommentFile(comment_id=None):
    try:
        if not Authenticator.route_access_check(request.path):
            return redirect(url_for('index'))
        files = CommentFile.query.filter(CommentFile.comment_id==comment_id).all()
        filePath = join(dirname(realpath(__file__)))+'/../static/uploads/'
        if len(files)==1:
            Logger.success(request.path)
            return send_file(filePath+files[0].file, attachment_filename=files[0].file, as_attachment=True)
        else:
            zipFileName = 'comment'+str(comment_id)+'.zip'
            Logger.success(request.path)
            return send_file(filePath+zipFileName, mimetype='application/zip', attachment_filename=zipFileName, as_attachment=True)
    except Exception as error:
        Logger.fail(request.path, error)
        return redirect(url_for('index'))

@app.route('/download_all_cases_csv', methods=['GET', 'POST'])
@login_required
def downloadAllCases():
    try:
        if not Authenticator.route_access_check(request.path):
            return redirect(url_for('index'))
        si = StringIO()
        writer = csv.DictWriter(si, fieldnames=['threat_id', 'title', 'category', 'status', 'description', 'steps', 'reported_time', 'user', 'user_role', 'email'])
        row_data = {"threat_id":"threat_id", "title":"title", "category":"category", "status":"status", "description":"description", "steps":"steps", "reported_time":"reported_time", "user":"user", "user_role":"user_role", "email":"email"}
        writer.writerow(row_data)
        if current_user.role_id == 1:
            threats = db.session.query(Threat, ThreatStatus, ThreatCategory, User, UserRole).join(ThreatStatus).join(ThreatCategory).join(User).join(UserRole).filter(UserRole.id==current_user.role_id).group_by(Threat).all()
        else: 
            threats = db.session.query(Threat, ThreatStatus, ThreatCategory, User, UserRole).join(ThreatStatus).join(ThreatCategory).join(User).join(UserRole).group_by(Threat).all()
        for threat in threats:
            row_data = {"threat_id":threat.Threat.id,
                            "title": threat.Threat.title,
                            "category": threat.ThreatCategory.category,
                            "status": threat.ThreatStatus.status,
                            "description": threat.Threat.description,
                            "steps": threat.Threat.reproduce_steps,
                            "reported_time": threat.Threat.timestamp,
                            "user": threat.User.first_name+' '+threat.User.surname,
                            "user_role": threat.UserRole.role,
                            "email": threat.User.email
                        }
            writer.writerow(row_data)
        output = make_response(si.getvalue())
        current_date = datetime.datetime.now().strftime('%Y%m%d')
        output.headers["Content-Disposition"] = "attachment; filename=threats_{}.csv".format(current_date)
        output.headers["Content-type"] = "text/csv"
        Logger.success(request.path)
        return output
    except Exception as error:
        Logger.fail(request.path, error)
        return redirect(url_for('index'))
