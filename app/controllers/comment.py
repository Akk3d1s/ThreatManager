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
def request_file_validation():
    file_list = request.files.getlist('file')
    print(file_list)
    if len(file_list)>20: # must be less than 20 files
        flash("Over than 20 files")
        return False
    file_size = 0
    for file in file_list: # loop to calculate the size of all the files uploaded
        file.seek(0, os.SEEK_END)
        file_size += file.tell()
        if file_size > ALLOWED_FILES_SIZE:
            flash("Size of files over the limit of 10 MB")
            return False
        if allowed_file(file.filename) == False:
            flash("Invalid file type")
            return False
    return True

# zip the files if the number of files are more than one
# considering a user can only download one file each time 
def request_file_save_zip(comment_id): 
    file_count = len(request.files.getlist('file'))
    if file_count == 1: # single file no need zip
        file = request.files['file']
        filename = "comment"+str(comment_id)+"_"+secure_filename(file.filename)
        file.seek(0)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file = CommentFile(file=filename, comment_id=comment_id)
        db.session.add(file)
        db.session.commit()
        return redirect(url_for('threat'))
    elif file_count > 1: # multiple file require zip file to be generated
        file_path = join(dirname(realpath(__file__)))+'/../static/uploads'
        zip_obj = ZipFile(file_path + '/comment'+str(comment_id)+'.zip', 'w')
        for file in request.files.getlist('file'):
            filename = "comment"+str(comment_id)+"_"+secure_filename(file.filename)
            file.seek(0)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            zip_obj.write(file_path+'/'+filename, basename(file_path+'/'+filename))
            file = CommentFile(file=filename, comment_id=comment_id)
            db.session.add(file)
            db.session.commit()
        zip_obj.close()
        return redirect(url_for('threat'))

# validate threat_id is exist first
# if user is citizen, validate if the citizen is the reporter of the threat first
# since a citizen can only access and comment on the threat related to herself/himself
<<<<<<< HEAD
def validateThreatIDnCitizen(threat_id):
    if Threat.query.filter_by(id=threat_id).first() is not None: 
        if current_user.role_id == 1:
            if not current_user.id == Threat.query.filter_by(id=threat_id).first().user_id:
                flash('Unauthorized Threat')
                return False
        return True
    flash('Invalid ID of Threat')
    return False
=======
def validate_citizen(threat_id):
    if current_user.role_id == 1:
        if not current_user.id == Threat.query.filter_by(id=threat_id).first().user_id:
            flash('Unauthorized Threat')
            return False
    return True
>>>>>>> Jonny

@app.route('/comment/<int:threat_id>', methods=['GET', 'POST'])
@login_required
def comment(threat_id=None):
    try:
        if not Authenticator.route_access_check(request.path):
            return redirect(url_for('index'))
<<<<<<< HEAD
        if not validateThreatIDnCitizen(threat_id): 
=======
        if not validate_citizen(threat_id): 
>>>>>>> Jonny
            return redirect(url_for('index'))
        form = ThreatCommentForm()
        if form.validate_on_submit():
            if request.files['file'].filename!='':
                if not request_file_validation():
                    return redirect(url_for('threat'))
            comment = Comment(comment=form.comment.data, user_id=current_user.id, threat_id=threat_id)
            db.session.add(comment)
            db.session.commit()
            if request.files['file'].filename!='':
                request_file_save_zip(comment.id)
            Logger.success(request.path)
            return redirect(url_for('threat'))
        flash('Empty comment')
        return redirect(url_for('threat'))
    except Exception as error:
        Logger.fail(request.path, error)
        return redirect(url_for('threat'))
