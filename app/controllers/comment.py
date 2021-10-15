from flask import render_template, flash, redirect, url_for, request
from app import ALLOWED_EXTENSIONS, app, db
from app.forms import ThreatCommentForm
from flask_login import current_user
from app.models.comment import Comment
from app.models.file import CommentFile
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath, basename
from zipfile import ZipFile
import os


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def requestFileValidation():
    if len(request.files.getlist('file'))>20:
        flash("More than 20 files")
        return redirect(url_for('threat'))
    for file in request.files.getlist('file'):
        print('validating files')
        if file:
            filename = secure_filename(file.filename)
            if allowed_file(filename) == False:
                print("false extension")
                flash("Invalid file type")
                return redirect(url_for('threat'))

def requestFileSaveZip(comment_id):
    fileCount = len(request.files.getlist('file'))
    if fileCount == 1:
        for file in request.files.getlist('file'):
            filename = "comment"+str(comment_id)+"_"+secure_filename(file.filename)
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
            # if file and allowed_file(filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            zipObj.write(filePath+'/'+filename, basename(filePath+'/'+filename))
            file = CommentFile(file=filename, comment_id=comment_id)
            db.session.add(file)
            db.session.commit()
        zipObj.close()
        return redirect(url_for('threat'))


@app.route('/comment/<int:threat_id>', methods=['GET', 'POST'])
def comment(threat_id=None):
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    form = ThreatCommentForm()
    if form.validate_on_submit():
        if len(request.files.getlist('file'))!=0:
            requestFileValidation()
        comment = Comment(comment=form.comment.data, user_id=current_user.id, threat_id=threat_id)
        db.session.add(comment)
        db.session.commit()
        requestFileSaveZip(comment.id)
    return redirect(url_for('threat'))

# @app.route('/comment/<int:threat_id>', methods=['GET', 'POST'])
# def comment(threat_id=None):
#     # if current_user.is_authenticated:
#     #     return redirect(url_for('index'))
#     form = ThreatCommentForm()
#     if form.validate_on_submit():
#         comment = Comment(comment=form.comment.data, user_id=current_user.id, threat_id=threat_id)
#         db.session.add(comment)
#         db.session.commit()
#         return redirect(url_for('threat'))
#     return redirect(url_for('threat'))

# @app.route('/comment/<int:threat_id>', methods=['GET', 'POST'])
# def comment(threat_id=None):
#     # if current_user.is_authenticated:
#     #     return redirect(url_for('index'))
#     form = ThreatCommentForm()
#     if form.validate_on_submit():
#         fileCount = 0
#         print(request.files.getlist('file'))
#         # check extensions and number of files first
#         if len(request.files.getlist('file'))!=0:
#             if len(request.files.getlist('file'))>20:
#                 flash("More than 20 files")
#                 return render_template('threat.html', title='Threat', form=form)
#             for file in request.files.getlist('file'):
#                 filename = secure_filename(file.filename)
#                 if allowed_file(filename) == False:
#                     print("false extension")
#                     flash("Invalid file type")
#                     return render_template('threat.html', title='Threat', form=form)
#                 fileCount = fileCount+1
#         comment = Comment(comment=form.comment.data, user_id=current_user.id, threat_id=threat_id)
#         db.session.add(comment)
#         db.session.commit()
#         if fileCount == 1:
#             for file in request.files.getlist('file'):
#                 filename = "comment"+str(comment.id)+"_"+secure_filename(file.filename)
#                 file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#                 file = CommentFile(file=filename, comment_id=comment.id)
#                 db.session.add(file)
#                 db.session.commit()
#             return redirect(url_for('threat'))
#         elif fileCount > 1:
#             filePath = join(dirname(realpath(__file__)))+'/../static/uploads'
#             zipObj = ZipFile(filePath + '/comment'+str(comment.id)+'.zip', 'w')
#             for file in request.files.getlist('file'):
#                 filename = "comment"+str(comment.id)+"_"+secure_filename(file.filename)
#                 # if file and allowed_file(filename):
#                 file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#                 zipObj.write(filePath+'/'+filename, basename(filePath+'/'+filename))
#                 file = CommentFile(file=filename, comment_id=comment.id)
#                 db.session.add(file)
#                 db.session.commit()
#             zipObj.close()
#             return redirect(url_for('threat'))
#     return redirect(url_for('threat'))