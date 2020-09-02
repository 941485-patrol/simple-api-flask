from models.employee import Employee
from controllers.employee.main import bp
from flask import (request, url_for, jsonify)
from middlewares import login_required
from flask.helpers import make_response
from controllers.helpers.responser import responser

@bp.route('/view/<int:id>', methods=['GET'])
@login_required
def view(id):
    emp=Employee.query.filter_by(id=id).first_or_404(description="Employee not found")
    empObj=emp.serialize()
    if emp.occupations is not None:
        empObj['occupation'] = {
            'occupation_name': emp.occupations.name,
            'occupation_description': emp.occupations.description,
            'this': url_for('occupations.view', id=emp.occupations.id),
        }
    else:
        empObj['occupation'] = None
    empObj['home']=url_for('employees.index')
    empObj['this']=request.path
    return responser(jsonify(empObj), 200)