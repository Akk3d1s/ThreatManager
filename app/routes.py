from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, ThreatReportForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Threat, ThreatStatus, ThreatCategory
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required
def index():
    # citizen role
    if current_user.role_id == 10:
        # threats = current_user.threats
        threats = db.session.query(User, Threat).filter(User.id == Threat.user_id).filter(User.id == current_user.id).all()
        return render_template("citizen.html", title='Home Page', threats=threats)
    # police roles
    else:
        threats = db.session.query(User, Threat, ThreatStatus, ThreatCategory).filter(User.id==Threat.user_id).filter(Threat.status_id==ThreatStatus.id).filter(Threat.category_id==ThreatCategory.id).all()
        # threats = db.session.query(User, Threat).filter(User.id == Threat.user_id).filter(User.id == current_user.id).all()

        return render_template("editor.html", title='Home Page', threats=threats)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

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

@app.route('/report', methods=['GET', 'POST'])
def report():
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    form = ThreatReportForm()
    if form.validate_on_submit():
        threat = Threat(title=form.title.data, description=form.description.data, recreation_steps=form.recreation_steps.data, user_id=current_user.id, status_id=1, category_id=1, attachment_id=1)
        db.session.add(threat)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('report.html', title='Report', form=form)

@app.route('/start/<int:threat_id>', methods=['GET', 'POST'])
def start(threat_id=None):
    threat = Threat.query.filter_by(id=threat_id).first()
    threat.status_id = 2
    db.session.commit()
    return redirect(url_for('index'))
