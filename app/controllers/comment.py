from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import ThreatCommentForm
from flask_login import current_user
from app.models.comment import Comment


@app.route('/comment/<int:threat_id>', methods=['GET', 'POST'])
def comment(threat_id=None):
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    form = ThreatCommentForm()
    if form.validate_on_submit():
        comment = Comment(comment=form.comment.data, user_id=current_user.id, threat_id=threat_id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('index'))
    return redirect(url_for('index'))

    # return redirect(url_for('index'))
