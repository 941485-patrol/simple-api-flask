from flask import (request, jsonify, session)
from controllers.user.main import bp

@bp.route('/logout')
def logout():
    session.clear()
    return jsonify({'message':'You are now logged out.'}), 200