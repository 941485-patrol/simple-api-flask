from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify)
from app import db
from models import Occupation, Employee
from forms import JobForm
import datetime
import pytz

bp=Blueprint('occupations', __name__, url_prefix='/jobs')

@bp.route('/', methods=('GET','POST'))
def index():
    if request.method=='POST':
        timezone=pytz.timezone('UTC')
        datenow = timezone.localize(datetime.datetime.utcnow())
        created_at=datenow.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        updated_at=datenow.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        form = JobForm()
        if form.validate_on_submit():
            job=Occupation(name=form.name.data, description=form.description.data, created_at=created_at, updated_at=updated_at)
            db.session.add(job)
            db.session.commit()
            return jsonify({'message':'Job created.','job_id':job.id})
        else:
            return jsonify({'errors': form.errors})

    elif request.method=='GET':
        jobs=Occupation.query.order_by(Occupation.id).all()
        jobList=[]
        for job in jobs:
            empList=[]
            for employee in job.employees:
                empObj={
                    'id':employee.id,
                    'name':employee.name,
                    'email':employee.email,
                }
                empList.append(empObj)
            jobObj=job.serialize()
            jobObj['employees']=empList
            jobList.append(jobObj)
        return jsonify(jobList)

@bp.route('/view/<int:id>', methods=['GET'])
def view(id):
    job=Occupation.query.filter_by(id=id).first_or_404(description="Job not found")
    return jsonify(job.serialize())

@bp.route('/update/<int:id>', methods=['POST'])
def update(id):
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    updated_at=datenow.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    form = JobForm()
    if form.validate_on_submit():
        job=Occupation.query.filter_by(id=id).update({'name':form.name.data, 'description':form.description.data, 'updated_at':updated_at})
        db.session.commit()
        return redirect(url_for('occupations.view',id=id))
    else:
        return jsonify({'errors': form.errors})

@bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    job=Occupation.query.filter_by(id=id).first_or_404(description="Job not found")
    db.session.delete(job)
    db.session.commit()
    return jsonify({'message':'Job deleted', 'home': request.url_root+'jobs'})