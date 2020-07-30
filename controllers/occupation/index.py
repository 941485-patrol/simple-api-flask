from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify)
from app import db
from models import Occupation
from controllers.occupation.main import bp
from forms import JobForm
from controllers.url_util import url_util
from middlewares import login_required
import datetime
import pytz
@bp.route('/', methods=('GET','POST'))
@login_required
def index():
    if request.method=='POST':
        timezone=pytz.timezone('UTC')
        datenow = timezone.localize(datetime.datetime.utcnow())
        form = JobForm()
        if form.validate_on_submit():
            job=Occupation(name=form.name.data, description=form.description.data, created_at=datenow, updated_at=datenow)
            db.session.add(job)
            db.session.commit()
            return jsonify({'message':'Job created.','job_id':job.id}), 200
        else:
            return jsonify({'errors': form.errors}), 400
    elif request.method=='GET':
        page=request.args.get('page',1)
        jobs=Occupation.query.order_by(Occupation.id).paginate(page=int(page),per_page=1)
        if len(jobs.items) == 0:
            return jsonify({'message': 'No data.'}), 200
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
        return jsonify(jobList), 200