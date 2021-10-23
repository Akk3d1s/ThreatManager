from flask import flash, redirect, url_for, request
from flask_login import login_required
from app import ALLOWED_EXTENSIONS, ALLOWED_FILES_SIZE, app, db
from app.forms import ThreatCommentForm
from flask_login import current_user
from app.models.comment import Comment
from app.models.file import CommentFile
from app.models.threat import Threat
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath, basename
from zipfile import ZipFile
import os
from app.helpers.authenticator import Authenticator
from app.helpers.logger import Logger


def allowed_file(filename): # check extension of the files
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# validate of all the files uploaded
def requestFileValidation():
    fileList = request.files.getlist('file')
    print(fileList)
    if len(fileList)>20: # must be less than 20 files
        flash("Over than 20 files")
        return False
    fileSize = 0
    for file in fileList: # loop to calculate the size of all the files uploaded
        file.seek(0, os.SEEK_END)
        fileSize += file.tell()
        if fileSize > ALLOWED_FILES_SIZE:
            flash("Size of files over the limit of 10 MB")
            return False
        if allowed_file(file.filename) == False:
            flash("Invalid file type")
            return False
    return True

# zip the files if the number of files are more than one
# considering a user can only download one file each time 
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
    elif fileCount > 1: # multiple file require zip file to be generated
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

# validate threat_id is exist first
# if user is citizen, validate if the citizen is the reporter of the threat first
# since a citizen can only access and comment on the threat related to herself/himself
def validateThreatIDnCitizen(threat_id):
    if Threat.query.filter_by(id=threat_id).first() is not None: 
        if current_user.role_id == 1:
            if not current_user.id == Threat.query.filter_by(id=threat_id).first().user_id:
                flash('Unauthorized Threat')
                return False
        return True
    flash('Invalid ID of Threat')
    return False

@app.route('/comment/<int:threat_id>', methods=['GET', 'POST'])
@login_required
def comment(threat_id=None):
    try:
        if not Authenticator.route_access_check(request.path):
            return redirect(url_for('index'))
        if not validateThreatIDnCitizen(threat_id): 
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
        flash('Empty comment')
        return redirect(url_for('threat'))
    except Exception as error:
        Logger.fail(request.path, error)
        return redirect(url_for('threat'))
