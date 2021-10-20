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


@app.route('/login')
def login():
    auth = request.authorization

    if auth:
        user = User.query.filter_by(email=auth.username).first()
        
        if user is not None and user.check_password(auth.password):
            token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)}, app.config['SECRET_KEY'])
            return jsonify({'token': token})
    
    return make_response('Invalid credentials', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

@app.route('/protected')
@token_required
def protected():
    return jsonify({'message': 'You have access!'})


from app.models.user import User