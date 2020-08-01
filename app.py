import os, datetime
from config import DevelopmentConfig
from os import environ
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(environ.get('APP_SETTINGS'))
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=3)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
db = SQLAlchemy(app)

from models import Occupation,Employee,User
from controllers import occupation,employee,user

app.register_blueprint(occupation.bp)
app.register_blueprint(employee.bp)
app.register_blueprint(user.bp)
# app.add_url_rule('/', endpoint='index')

from middlewares import login_required

@app.route("/")
def hello():
    return "Hello World"

if __name__ == '__main__':
    app.run()