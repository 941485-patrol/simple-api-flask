from models.employee import Employee
from app import db
from flask import (url_for, jsonify)
from controllers.employee.main import bp

@bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    emp=Employee.query.filter_by(id=id).first_or_404(description="Employee not found")
    db.session.delete(emp)
    db.session.commit()
    return jsonify({'message':'Employee deleted.', 'home': url_for('employees.index')}), 200