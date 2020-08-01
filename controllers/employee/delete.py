from models.employee import Employee
from app import db
from flask import (url_for, jsonify, request)
from controllers.employee.main import bp
from middlewares import login_required
from controllers.helpers import responser

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    emp=Employee.query.filter_by(id=id).first_or_404(description="Employee not found")
    db.session.delete(emp)
    db.session.commit()
    return responser(jsonify({'message':'Employee deleted.', 'home': url_for('employees.index')}), 200)