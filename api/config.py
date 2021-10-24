'''API Config'''
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    '''Default values to be set if .flaskenv has not been set'''
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess-api-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, '../app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(basedir, '../app/static/uploads')
    FLASK_ENV = 'development'
