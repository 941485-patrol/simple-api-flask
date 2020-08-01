from flask import (url_for, jsonify, request)
from controllers.occupation.main import bp
from app import db
from models import Occupation
from middlewares import login_required
from controllers.helpers import responser

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    job=Occupation.query.filter_by(id=id).first_or_404(description="Job not found")
    db.session.delete(job)
    db.session.commit()
    return responser(jsonify({'message':'Job deleted.', 'home': url_for('occupations.index')}), 200)