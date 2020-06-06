from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify)
from app import db
from models import Employee
import datetime
import pytz

bp=Blueprint('employees', __name__, url_prefix='/employees')

@bp.route('/', methods=('GET','POST'))
def index():
    if request.method=='POST':
        timezone=pytz.timezone('UTC')
        datenow = timezone.localize(datetime.datetime.utcnow())
        name=request.form['name']
        email=request.form['email']
        occupations_id=request.form['occupations_id']
        created_at=datenow.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        updated_at=datenow.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        emp=Employee(name=name, email=email, occupations_id=occupations_id, created_at=created_at, updated_at=updated_at)
        db.session.add(emp)
        db.session.commit()
        return jsonify({'message':'Emloyee created.','employee_id':emp.id})

    elif request.method=='GET':
        employees=Employee.query.order_by(Employee.id).all()
        empList=[]
        for employee in employees:
            empObj = employee.serialize()
            empObj['occupation_name'] = employee.occupations.name
            empObj['occupation_description'] = employee.occupations.description
            empList.append(empObj)
        return jsonify(empList)

@bp.route('/view/<int:id>', methods=['GET'])
def view(id):
    emp=Employee.query.filter_by(id=id).first_or_404(description="Employee not found")
    empObj=emp.serialize()
    empObj['occupation_name'] = emp.occupations.name
    empObj['occupation_description'] = emp.occupations.description
    return jsonify(empObj)

@bp.route('/update/<int:id>', methods=['POST'])
def update(id):
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    name=request.form['name']
    email=request.form['email']
    occupations_id=request.form['occupations_id']
    updated_at=datenow.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    emp=Employee.query.filter_by(id=id).update({'name':name, 'email':email, 'occupations_id':occupations_id, 'updated_at':updated_at})
    db.session.commit()
    return redirect(url_for('employees.view',id=id))

@bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    emp=Employee.query.filter_by(id=id).first_or_404(description="Employee not found")
    db.session.delete(emp)
    db.session.commit()
    return jsonify({'message':'Employee deleted', 'home': request.url_root+'employees'})