from flask import (redirect, url_for, jsonify, request)
from app import db
from models import Occupation
from controllers.occupation.main import bp
from forms import JobForm
from middlewares import login_required
import datetime
import pytz
from controllers.helpers.responser import responser

@bp.route('/update/<int:id>', methods=['POST'])
@login_required
def update(id):
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    form = JobForm()
    if form.validate_on_submit():
        job=Occupation.query.filter_by(id=id).update({'name':form.name.data, 'description':form.description.data, 'updated_at':datenow})
        db.session.commit()
        return responser(redirect(url_for('occupations.view',id=id)), 200)
    else:
        return responser(jsonify({'errors': form.errors}), 400)
