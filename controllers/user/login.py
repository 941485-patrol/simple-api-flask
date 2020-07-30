from forms import LoginForm
from models import User
from flask import (request, jsonify, session)
from werkzeug.security import check_password_hash
from controllers.user.main import bp
from app import app
import datetime

@bp.route('/login', methods=('GET','POST'))
def login():
    if request.method == 'POST':
        form = LoginForm()
        if form.validate_on_submit():
            return jsonify({'message':'You are now logged in.'}), 200
        else:
            return jsonify({'errors': form.errors}), 400
        # form = LoginForm()
        # if form.validate_on_submit():
        #     username=form.username.data
        #     password=form.password.data
        #     isUserExists=User.query.filter_by(username=username).first()
        #     if isUserExists:
        #         pwhash=isUserExists.password
        #         isPassCorrect=check_password_hash(pwhash,password)
        #         if isPassCorrect==True:
        #             session.clear()
        #             session['user_id'] = isUserExists.id
        #             return jsonify({'message':'You are now logged in.'})
        #         else:
        #             return jsonify({'error':'Wrong password.'})
        #     else:
        #         return jsonify({'error':'Wrong credentials.'}),400
        # else:
        #     return jsonify({'errors': form.errors})