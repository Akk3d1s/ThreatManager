import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Flask and some of its extensions use the value of the secret key as a cryptographic key,
    useful to generate signatures or tokens. The Flask-WTF extension uses it to protect web
    forms against a nasty attack called Cross-Site Request Forgery or CSRF (pronounced "seasurf").
    As its name implies, the secret key is supposed to be secret, as the strength of the tokens
    and signatures generated with it depends on no person outside of the trusted maintainers of the
    application knowing it."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False