from flask import (Blueprint, session, g, request)
from models import User

bp=Blueprint('users', __name__, url_prefix='/users')

@bp.before_app_request
def get_current_user():
    current_user=session.get('user_id',None)
    if current_user is None:
        g.user=None
    else:
        g.user=User.query.get_or_404(current_user)

@bp.after_app_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin')
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response