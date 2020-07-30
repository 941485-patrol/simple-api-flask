from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify)
from app import db
from models import Employee
from forms import EmployeeForm
from controllers.url_util import url_util
from controllers.employee.main import bp
import datetime
import pytz
from middlewares import login_required

@bp.route('/', methods=('GET','POST'))
@login_required
def index():
    if request.method=='POST':
        timezone=pytz.timezone('UTC')
        datenow = timezone.localize(datetime.datetime.utcnow())
        form = EmployeeForm()
        if form.validate_on_submit():
            emp=Employee(name=form.name.data, email=form.email.data, occupations_id=form.occupations_id.data, created_at=datenow, updated_at=datenow)
            db.session.add(emp)
            db.session.commit()
            return jsonify({'message':'Employee created.','employee_id':emp.id}), 200
        else:
            return jsonify({'errors': form.errors}), 400
    elif request.method=='GET':
        page=request.args.get('page',1)
        employees=Employee.query.order_by(Employee.id).paginate(page=int(page),per_page=1)
        if len(employees.items) == 0:
           return jsonify({'message': 'No data.'}), 200
        else:
            empList={}
            empResult=[]
            empList['navi']=url_util(employees, 'employees.index')
            for employee in employees.items:
                empObj = employee.serialize()
                empObj['occupation']={
                    'occupations_name': employee.occupations.name,
                    'occupations_description': employee.occupations.description,
                    'this': url_for('occupations.view',id=employee.occupations.id),
                }
                empResult.append(empObj)
            empList['results']=empResult
            return jsonify(empList), 200