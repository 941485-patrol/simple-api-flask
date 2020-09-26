from flask import (Blueprint, flash, g, render_template, request, session, url_for, jsonify)
from app import db
from models import Occupation, Employee
from controllers.occupation.main import bp
from forms import JobForm
from controllers.url_util import url_util
from middlewares import login_required
import datetime
import pytz
from controllers.helpers import responser
from controllers.helpers.jobSearcher import jobSearcher
from controllers.helpers.jobSorter import jobSorter

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
            return responser(jsonify({'message':'Job created.','job_id':job.id}), 200)
        else:
            return responser(jsonify({'errors': form.errors}), 400)
    elif request.method=='GET':
        page=request.args.get('page',1)
        sort=request.args.get('sort','id')
        searchee=request.args.get('search',None)
        searchKey=jobSearcher(searchee)
        sortColumn=jobSorter(sort)
        if sortColumn is None:
            return responser(jsonify({'message':'Wrong sorting order.'}), 400)
        jobs=Occupation.query.filter(searchKey).order_by(sortColumn).paginate(page=int(page),per_page=5)
        # jobs = db.session.query(Occupation).outerjoin(Employee).filter(searchKey).order_by(sortColumn).paginate(page=int(page),per_page=5)
        if len(jobs.items) == 0:
            return responser(jsonify({'message': 'No data.'}), 200)
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
        return responser(jsonify(jobList), 200)