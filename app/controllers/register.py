from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import RegistrationForm
from flask_login import current_user
from app.models.user import User

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(firstname=form.firstname.data, surename=form.surename.data, email=form.email.data, role_id=1)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)