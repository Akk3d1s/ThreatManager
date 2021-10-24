"""API credentials"""
from flask import render_template, request, redirect, url_for
from flask_login import login_required
from app import app
from app.helpers.authenticator import Authenticator
from app.helpers.logger import Logger


@app.route('/api_credential')
@login_required
def api_credential():
    """API credential route. Can only be accessed be the developer role"""
    try:
        if not Authenticator.route_access_check(request.path):
            return redirect(url_for('index'))
        return render_template("api_credential.html")
    except Exception as error:
        Logger.fail(request.path, error)
        return redirect(url_for('index'))
