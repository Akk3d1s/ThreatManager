from app import app
import jwt
import datetime
from functools import wraps
from flask import jsonify, request, make_response, send_from_directory
# bootstrapping
from app.models.user import User
from app.models.user_role import UserRole
from app.models.threat import Threat
from app.models.threat_file import ThreatFile
from app.models.threat_comment import ThreatComment
from app.helpers.logger import Logger
from app.models.threat_status import ThreatStatus
from app.models.threat_category import ThreatCategory


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

    try:        
        if auth:
            user = User.query.filter_by(email=auth.username, role_id=5).first()
            
            if user is not None and user.check_password(auth.password):
                token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)}, app.config['SECRET_KEY'])
                Logger.success('/login', 'Retrieve token', user.id)
                return jsonify({'token': token})
        
        return make_response('Invalid credentials', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    except Exception as err:
        Logger.fail('/login', str(err), get_user_id())
        return jsonify({'error': 'Something went wrong, please contact support'}), 500


@app.route('/threats')
@token_required
def threats():
    try:
        threats = Threat.query.all()
        Logger.success('/threats', 'Retrieve threats', get_user_id())
        return jsonify(threats)
    except Exception as err:
        Logger.fail('/login', str(err), get_user_id())
        return jsonify({'error': 'Something went wrong, please contact support'}), 500


@app.route('/threats/<threat_id>/files')
@token_required
def threat_files(threat_id):
    try:
        files = ThreatFile.query.filter_by(threat_id=threat_id).all()
        Logger.success('/files', 'Retrieve files', get_user_id())
        return jsonify(files)
    except Exception as err:
        Logger.fail('/files', str(err), get_user_id())
        return jsonify({'error': 'Something went wrong, please contact support'}), 500


@app.route('/threats/<threat_id>/files/<file_id>/download')
@token_required
def threat_file_download(threat_id, file_id):
    try:
        file = ThreatFile.query.filter_by(threat_id=threat_id, id=file_id).first()
        if file is None or file.file is None:
            message = 'Unable to locate file'
            Logger.fail('/download', message, get_user_id())
            return jsonify({'error': message}), 404
        Logger.success('/download', 'Download files', get_user_id())
        return send_from_directory(app.config['UPLOAD_FOLDER'], file.file, as_attachment=True)
    except Exception as err:
        Logger.fail('/download', str(err), get_user_id())
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
                Logger.fail('/comments', 'Unable to locate user', get_user_id())
                return jsonify({'error': 'Something went wrong, please contact support'}), 500
            response.append({'comment': comment.comment, 'created_at': comment.created_at, 'role': user.role.role})
        Logger.success('/comments', 'Retrieve comments', get_user_id())
        return jsonify(response)
    except Exception as err:
        Logger.fail('/comments', str(err), get_user_id())
        return jsonify({'error': 'Something went wrong, please contact support'}), 500


def get_user_id():
    data = jwt.decode(request.args.get('token'), app.config['SECRET_KEY'], algorithms=['HS256'])
    user = User.query.filter_by(email=data['user']).first()
    if user is None:
        return None
    return user.id