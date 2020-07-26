from flask import (redirect, url_for, jsonify)
from app import db
from models import Occupation
from controllers.occupation.main import bp
from forms import JobForm
import datetime
import pytz

@bp.route('/update/<int:id>', methods=['POST'])
def update(id):
    timezone=pytz.timezone('UTC')
    datenow = timezone.localize(datetime.datetime.utcnow())
    form = JobForm()
    if form.validate_on_submit():
        job=Occupation.query.filter_by(id=id).update({'name':form.name.data, 'description':form.description.data, 'updated_at':datenow})
        db.session.commit()
        return redirect(url_for('occupations.view',id=id)), 200
    else:
        return jsonify({'errors': form.errors}), 400
