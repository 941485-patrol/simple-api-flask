from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify)
from app import db
from models import Occupation, Employee
from forms import JobForm
from .url_util import url_util
import datetime
import pytz

bp=Blueprint('occupations', __name__, url_prefix='/jobs')

@bp.route('/', methods=('GET','POST'))
def index():
    if request.method=='POST':
        timezone=pytz.timezone('UTC')
        datenow = timezone.localize(datetime.datetime.utcnow())
        form = JobForm()
        if form.validate_on_submit():
            job=Occupation(name=form.name.data, description=form.description.data, created_at=datenow, updated_at=datenow)
            db.session.add(job)
            db.session.commit()
            return jsonify({'message':'Job created.','job_id':job.id})
        else:
            return jsonify({'errors': form.errors})
    elif request.method=='GET':
        page=request.args.get('page',1)
        jobs=Occupation.query.order_by(Occupation.id).paginate(page=int(page),per_page=1)
        jobList={}
        jobResult=[]
        jobList['navi']=url_util(jobs, 'occupations.index')
        for job in jobs.items:
            empList=[]
            for employee in job.employees:
                empObj={
                    'id':employee.id,
                    'name':employee.name,
                    'email':employee.email,
                    'this':url_for('employees.view',id=employee.id),
                }
                empList.append(empObj)
            jobObj=job.serialize()
            jobObj['this']=url_for('occupations.view',id=job.id)
            jobObj['employees']=empList
            jobResult.append(jobObj)
        jobList['results']=jobResult
        return jsonify(jobList)

@bp.route('/view/<int:id>', methods=['GET'])
def view(id):
    job=Occupation.query.filter_by(id=id).first_or_404(description="Job not found")
    jobObj=job.serialize()
    jobObj['home']=url_for('occupations.index')
    jobObj['this']=request.path
    return jsonify(jobObj)

@bp.route('/update/<int:id>', methods=['POST'])
def update(id):
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    form = JobForm()
    if form.validate_on_submit():
        job=Occupation.query.filter_by(id=id).update({'name':form.name.data, 'description':form.description.data, 'updated_at':datenow})
        db.session.commit()
        return redirect(url_for('occupations.view',id=id))
    else:
        return jsonify({'errors': form.errors})

@bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    job=Occupation.query.filter_by(id=id).first_or_404(description="Job not found")
    db.session.delete(job)
    db.session.commit()
    return jsonify({'message':'Job deleted', 'home': url_for('occupations.index')})