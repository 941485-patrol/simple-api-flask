from models.employee import Employee
from controllers.employee.main import bp
from flask import (request, url_for, jsonify)

@bp.route('/view/<int:id>', methods=['GET'])
def view(id):
    emp=Employee.query.filter_by(id=id).first_or_404(description="Employee not found")
    empObj=emp.serialize()
    empObj['occupation'] = {
        'occupation_name': emp.occupations.name,
        'occupation_description': emp.occupations.description,
        'this': url_for('occupations.view', id=emp.occupations.id),
    }
    empObj['home']=url_for('employees.index')
    empObj['this']=request.full_path
    return jsonify(empObj)