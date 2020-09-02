from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify)
from app import db
from models import Employee, Occupation
from forms import EmployeeForm
from controllers.url_util import url_util
from controllers.employee.main import bp
import datetime
import pytz
from middlewares import login_required
from controllers.helpers.responser import responser
from controllers.helpers.empSorter import empSorter
from controllers.helpers.empSearcher import empSearcher

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
            return responser(jsonify({'message':'Employee created.','employee_id':emp.id}), 200)
        else:
            return responser(jsonify({'errors': form.errors}), 400)
    elif request.method=='GET':
        page=request.args.get('page',1)
        sort=request.args.get('sort','id')
        searchee=request.args.get('search',None)
        searchKey=empSearcher(searchee)
        sortColumn=empSorter(sort)
        if sortColumn is None:
            return responser(jsonify({'message':'Wrong sorting order.'}), 400)
        # employees = db.session.query(Employee).outerjoin(Occupation).filter(searchKey).order_by(sortColumn).paginate(page=int(page),per_page=5)
        employees=Employee.query.filter(searchKey).order_by(sortColumn).paginate(page=int(page),per_page=5)
        if len(employees.items) == 0:
            return responser(jsonify({'message': 'No data.'}), 200)
        else:
            empList={}
            empResult=[]
            empList['navi']=url_util(employees, 'employees.index')
            for employee in employees.items:
                empObj = employee.serialize()
                if employee.occupations is not None:
                    empObj['occupation']={
                        'occupations_name': employee.occupations.name,
                        'occupations_description': employee.occupations.description,
                        'this': url_for('occupations.view',id=employee.occupations.id),
                    }
                else:
                    empObj['occupation'] = None
                empObj['this']=url_for('employees.view',id=employee.id)
                empResult.append(empObj)
            empList['results']=empResult
            return responser(jsonify(empList), 200)