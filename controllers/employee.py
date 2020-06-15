from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify)
from app import db
from models import Employee
from forms import EmployeeForm
from .url_util import url_util
import datetime
import pytz

bp=Blueprint('employees', __name__, url_prefix='/employees')

@bp.route('/', methods=('GET','POST'))
def index():
    if request.method=='POST':
        timezone=pytz.timezone('UTC')
        datenow = timezone.localize(datetime.datetime.utcnow())
        form = EmployeeForm()
        if form.validate_on_submit():
            emp=Employee(name=form.name.data, email=form.email.data, occupations_id=form.occupations_id.data, created_at=datenow, updated_at=datenow)
            db.session.add(emp)
            db.session.commit()
            return jsonify({'message':'Emloyee created.','employee_id':emp.id})
        else:
            return jsonify({'errors': form.errors})
    elif request.method=='GET':
        page=request.args.get('page',1)
        employees=Employee.query.order_by(Employee.id).paginate(page=int(page),per_page=1)
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
        return jsonify(empList)

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
    empObj['this']=request.path
    return jsonify(empObj)

@bp.route('/update/<int:id>', methods=['POST'])
def update(id):
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    form = EmployeeForm()
    if form.validate_on_submit():
        emp=Employee.query.filter_by(id=id).update({'name':form.name.data, 'email':form.email.data, 'occupations_id':form.occupations_id.data, 'updated_at':datenow})
        db.session.commit()
        return redirect(url_for('employees.view',id=id))
    else:
        return jsonify({'errors': form.errors})

@bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    emp=Employee.query.filter_by(id=id).first_or_404(description="Employee not found")
    db.session.delete(emp)
    db.session.commit()
    return jsonify({'message':'Employee deleted', 'home': url_for('employees.index')})