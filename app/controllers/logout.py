"""
Contains a function handling a user logging out.
"""
from flask import redirect, url_for
from app import app
from flask_login import logout_user

@app.route('/logout')
def logout():
    """Handle logout"""
    try:
        logout_user()
        return redirect(url_for('index'))
    except ValueError as error:
        print(error)
