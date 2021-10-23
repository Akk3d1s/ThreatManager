from app import app
import jwt
import datetime
from functools import wraps
from flask import jsonify, request, make_response, send_from_directory
# bootstrapping
from app.models.user import User
from app.models.user_role import UserRole
from app.models.threat import Threat
from app.models.threat_status import ThreatStatus
from app.models.threat_category import ThreatCategory
from app.models.threat_file import ThreatFile
from app.models.threat_comment import ThreatComment

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
        return jsonify({'error': 'Something went wrong, please contact support'}), 500


@app.route('/threats')
@token_required
def threats():
    try:
        threats = Threat.query.all()
        return jsonify(threats)
    except Exception as err:
        # should log err to logging service
        return jsonify({'error': 'Something went wrong, please contact support'}), 500


@app.route('/threats/<threat_id>/files')
@token_required
def threat_files(threat_id):
    try:
        files = ThreatFile.query.filter_by(threat_id=threat_id).all()
        return jsonify(files)
    except Exception as err:
        # should log err to logging service
        return jsonify({'error': 'Something went wrong, please contact support'}), 500


@app.route('/threats/<threat_id>/files/<file_id>/download')
@token_required
def threat_file_download(threat_id, file_id):
    try:
        file = ThreatFile.query.filter_by(threat_id=threat_id, id=file_id).first()
        if file is None or file.file is None:
            return jsonify({'error': 'Unable to locate file'}), 404
        return send_from_directory(app.config['UPLOAD_FOLDER'], file.file, as_attachment=True)
    except Exception as err:
        # should log err to logging service
        return jsonify({'error': 'Something went wrong, please contact support'}), 500


@app.route('/threats/<threat_id>/comments')
@token_required
def threat_comments(threat_id):
    try:
        response = []
        comments = ThreatComment.query.filter_by(threat_id=threat_id).all()
        for comment in comments:
            user = User.query.filter_by(id=comment.user_id).first()
            if user is None:
                return jsonify({'error': 'Something went wrong, please contact support'}), 500
            response.append({'comment': comment.comment, 'created_at': comment.created_at, 'role': user.role.role})
        return jsonify(response)
    except Exception as err:
        # should log err to logging service
        return jsonify({'error': 'Something went wrong, please contact support'}), 500