from flask import send_file
from app import ALLOWED_EXTENSIONS, app, db
from flask_login import current_user
from app.models.threat import Threat
from app.models.file import ThreatFile, CommentFile
from werkzeug.utils import secure_filename, send_from_directory
from os.path import join, dirname, realpath, basename


@app.route('/download_file_threat/<int:threat_id>', methods=['GET', 'POST'])
def downloadThreatFile(threat_id=None):
    files = ThreatFile.query.filter(ThreatFile.threat_id==threat_id).all()
    filePath = join(dirname(realpath(__file__)))+'/../static/uploads/'
    if len(files)==1:
        return send_file(filePath+files[0].file, attachment_filename=files[0].file, as_attachment=True)
    else:
        zipFileName = 'threat'+str(threat_id)+'.zip'
        return send_file(filePath+zipFileName, mimetype='application/zip', attachment_filename=zipFileName, as_attachment=True)

@app.route('/download_file_comment/<int:comment_id>', methods=['GET', 'POST'])
def downloadCommentFile(comment_id=None):
    files = CommentFile.query.filter(CommentFile.comment_id==comment_id).all()
    filePath = join(dirname(realpath(__file__)))+'/../static/uploads/'
    if len(files)==1:
        return send_file(filePath+files[0].file, attachment_filename=files[0].file, as_attachment=True)
    else:
        zipFileName = 'comment'+str(comment_id)+'.zip'
        return send_file(filePath+zipFileName, mimetype='application/zip', attachment_filename=zipFileName, as_attachment=True)


