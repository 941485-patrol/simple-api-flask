from flask import (request, url_for, jsonify)
from controllers.occupation.main import bp
from models import Occupation
from middlewares import login_required
from flask.helpers import make_response
from controllers.helpers.responser import responser

@bp.route('/view/<int:id>', methods=['GET'])
@login_required
def view(id):
    job=Occupation.query.filter_by(id=id).first_or_404(description="Job not found")
    jobObj=job.serialize()
    empList=[]
    for employee in job.employees:
        empObj={
            'id':employee.id,
            'name':employee.name,
            'email':employee.email,
            'this':url_for('employees.view',id=employee.id),
        }
        empList.append(empObj)
    jobObj['employees']=empList
    jobObj['home']=url_for('occupations.index')
    jobObj['this']=request.path
    return responser(jsonify(jobObj), 200)