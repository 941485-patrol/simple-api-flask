from models.employee import Employee
from app import db
from flask import (request, redirect, url_for, jsonify)
from controllers.employee.main import bp
from models import Employee
from forms import EmployeeForm
import datetime
import pytz

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