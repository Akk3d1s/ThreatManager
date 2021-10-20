from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
import jwt
import datetime
from functools import wraps
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message': 'No token provided'}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except Exception as err:
            return jsonify({'message': 'Invalid token'}), 403

        return f(*args, **kwargs)

    return decorated


# @todo - should check if this account is a developer role
@app.route('/login')
def login():
    auth = request.authorization

    try:        
        if auth:
            user = User.query.filter_by(email=auth.username).first()
            
            if user is not None and user.check_password(auth.password):
                token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)}, app.config['SECRET_KEY'])
                return jsonify({'token': token})
        
        return make_response('Invalid credentials', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    except Exception as err:
        # should log err to logging service
        return jsonify({'error', 'Something went wrong, please contact support'})

@app.route('/threats')
@token_required
def threats():

    try:
        threats = Threat.query.all()
        return jsonify(threats)
    except Exception as err:
        # should log err to logging service
        return jsonify({'error', 'Something went wrong, please contact support'})



# bootstrapping
from app.models.user import User
from app.models.threat import Threat
from app.models.threat_status import ThreatStatus
from app.models.threat_category import ThreatCategory