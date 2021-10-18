from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required
from app import ALLOWED_EXTENSIONS, ALLOWED_FILES_SIZE, app, db
from app.forms import ThreatCommentForm
from flask_login import current_user
from app.models.comment import Comment
from app.models.file import CommentFile
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath, basename
from zipfile import ZipFile
import os
from app.helpers.authenticator import Authenticator
from app.helpers.logger import Logger


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def requestFileValidation():
    fileList = request.files.getlist('file')
    print(fileList)
    if len(fileList)>20:
        flash("More than 20 files")
        return False
    fileSize = 0
    for file in fileList:
        file.seek(0, os.SEEK_END)
        fileSize += file.tell()
        if fileSize > ALLOWED_FILES_SIZE:
            flash("Size of files over the limit of 5 MB")
            return False
        if allowed_file(file.filename) == False:
            flash("Invalid file type")
            return False
    return True

def requestFileSaveZip(comment_id):
    fileCount = len(request.files.getlist('file'))
    if fileCount == 1: # single file no need zip
        file = request.files['file']
        filename = "comment"+str(comment_id)+"_"+secure_filename(file.filename)
        file.seek(0)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file = CommentFile(file=filename, comment_id=comment_id)
        db.session.add(file)
        db.session.commit()
        return redirect(url_for('threat'))
    elif fileCount > 1:
        filePath = join(dirname(realpath(__file__)))+'/../static/uploads'
        zipObj = ZipFile(filePath + '/comment'+str(comment_id)+'.zip', 'w')
        for file in request.files.getlist('file'):
            filename = "comment"+str(comment_id)+"_"+secure_filename(file.filename)
            file.seek(0)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            zipObj.write(filePath+'/'+filename, basename(filePath+'/'+filename))
            file = CommentFile(file=filename, comment_id=comment_id)
            db.session.add(file)
            db.session.commit()
        zipObj.close()
        return redirect(url_for('threat'))


@app.route('/comment/<int:threat_id>', methods=['GET', 'POST'])
@login_required
def comment(threat_id=None):
    try:
        if not Authenticator.route_access_check(request.path):
            return redirect(url_for('index'))
        form = ThreatCommentForm()
        if form.validate_on_submit():
            if request.files['file'].filename!='':
                if not requestFileValidation():
                    return redirect(url_for('threat'))
            comment = Comment(comment=form.comment.data, user_id=current_user.id, threat_id=threat_id)
            db.session.add(comment)
            db.session.commit()
            if request.files['file'].filename!='':
                requestFileSaveZip(comment.id)
            Logger.success(request.path)
        return redirect(url_for('threat'))
    except Exception as error:
        Logger.fail(request.path, error)