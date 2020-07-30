from forms import RegisterForm
from app import db
from models import User
from flask import (request, jsonify)
from werkzeug.security import generate_password_hash
from controllers.user.main import bp
import pytz
import datetime

@bp.route('/register', methods=('GET','POST'))
def register():
    if request.method == 'POST':
        form = RegisterForm()
        if form.validate_on_submit():
            timezone=pytz.timezone('UTC')
            datenow = timezone.localize(datetime.datetime.utcnow())
            hashed_pass = generate_password_hash(form.password.data,method="pbkdf2:sha256", salt_length=8)
            usr=User(username=form.username.data, password=hashed_pass, created_at=datenow, updated_at=datenow)
            db.session.add(usr)
            db.session.commit()
            return jsonify({'message':'User created.','user_id':usr.id}), 200
        else:
            return jsonify({'errors': form.errors}), 400